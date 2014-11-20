---
layout: post.html
title: Redis Lua Scripting for Performance
summary: NoSQL tends to force a lot of data model logic into the app layer, making it hard (or even impossible) to optimize certain types of operations. By supporting server-side Lua scripting, Redis provides a way to move some of that logic back into the data layer without having to add higher-order operations to the API.
tags: [code]
---

Lately I've been working on [Zaqar's][2] new Redis driver. Zaqar provides a stateless REST API for creating and consuming message feeds. When there are multiple observers AKA subscribers of a feed, each observer uses a marker to keep track of its own position in that feed. 

In this design, there is a race condition that emerges as a result of the interplay between producers and observers, that can cause observers to miss one or more messages. This issue manifests differently depending on which backend you use with Zaqar, but generally speaking, to avoid the condition you need to make sure a message with a higher marker is never *persisted* before a message with a lower marker.

The way we originally dealt with this in the Redis driver was to use the server's support for transactions. To do this with Redis, you set a watch on a key (or set of keys) upon which the transaction depends, then prepare the transaction by creating a pipeline of commands, and finally attempt to execute that pipeline. An error will be raised if any of the watched keys have changed in the meantime, causing all commands to abort. 

Here is a version of the code in Zaqar that we originally used to post messages, edited for instructional purposes:

```python
with self._client.pipeline() as pipe:

    start_ts = timeutils.utcnow_ts()

    # NOTE(kgriffs): Retry the operation if another transaction
    # completes before this one, in which case it may have
    # posted messages with the same rank counter the current
    # thread is trying to use, which would cause messages
    # to get out of order and introduce the risk of a client
    # missing a message while reading from the queue.
    #
    # This loop will eventually time out if we can't manage to
    # post any messages due to other threads continually beating
    # us to the punch.

    # TODO(kgriffs): Add a backoff sleep between retries

    while (timeutils.utcnow_ts() - start_ts) < RETRY_POST_TIMEOUT:
        now = timeutils.utcnow_ts()
        prepared_messages = [
            Message(
                ttl=msg['ttl'],
                created=now,
                client_uuid=client_uuid,
                claim_id=None,
                claim_expires=now,
                body=msg.get('body', {}),
            )

            for msg in messages
        ]

        try:
            # NOTE(kgriffs): Keep an eye on the side counter; if
            # it changes, we know another parallel request beat us
            # to the punch and we need to get a new starting
            # value for rank_counter.
            pipe.watch(counter_key)

            rank_counter = pipe.get(counter_key)
            rank_counter = int(rank_counter) if rank_counter else 0

            pipe.multi()

            for i, msg in enumerate(prepared_messages):
                msg.to_redis(pipe)
                pipe.zadd(msgset_key, rank_counter + i, msg.id)

            pipe.incrby(counter_key, len(keys))
            pipe.execute()

        except redis.exceptions.WatchError:
            continue
```

As you can see, Zaqar uses an ordered set to index messages. It ranks the messages using a side counter. Elsewhere in the Redis driver, there is a method that lists messages. The client provides a marker which tells the server the position of the last message received by that client, and then the server is responsible for returning the next batch of messages for that client.

In the Redis driver, the marker is simply the message ID. In order to return to the client a list of messages *after* the specified marker, the service looks up the rank of that marker in the message index, then lists any subsequent messages, in rank order, up to a specified limit.

This works, but the more concurrent requests served, the more frequent the counter collisions. The result is a lot of wasted CPU capacity spent on retrying the operation, and significantly higher per-request latency. There are strategies that can reduce the number of retries (on average) required, but they only offer marginal improvements. 

Fortunately, there's a better way.

Since version 2.6, Redis supports server-side execution of Lua scripts. This is analogous to stored procedures in the RDBMS world. However, only one Redis script may run at a time, and no other commands may run concurrently. In this way you can execute a batch of commands atomically, without having to use watch-abort-retry loops in the client. On the other hand, this also means scripts must finish quickly to avoid starving other incoming commands.<sup><a name="id-1" href="#id-1.ftn">1</a></sup>

Generally speaking, NoSQL tends to force a lot of data model logic into the app layer. By supporting server-side Lua scripting, Redis provides a way to move some of that logic back into the data layer without having to add higher-order operations to the API.

All things considered, I had a hunch that moving the indexing logic to Lua would increase the performance of posting messages to the service. I was hoping for at least a moderate improvement over the transactional approach outlined above.

The first thing I noticed was that by moving much of the logic to Lua, I was able to greatly simplify the Python code:

```python
with self._client.pipeline() as pipe:
    message_ids = []
    now = timeutils.utcnow_ts()

    with self._client.pipeline() as pipe:
        for msg in messages:
            prepared_msg = Message(
                ttl=msg['ttl'],
                created=now,
                client_uuid=client_uuid,
                claim_id=None,
                claim_expires=now,
                body=msg.get('body', {}),
            )

            prepared_msg.to_redis(pipe)
            message_ids.append(prepared_msg.id)

        pipe.execute()

    # NOTE(kgriffs): If this call fails, we will return
    # an error to the client and the messages will be
    # orphaned, but Redis will remove them when they
    # expire, so we will just pretend they don't exist
    # in that case.
    self._index_messages(msgset_key, counter_key, message_ids)
```

The `_index_messages` method prepares the arguments, then passes them to the [cached Lua script][1]:

```python
def _index_messages(self, msgset_key, counter_key, message_ids):
    # NOTE(kgriffs): A watch on a pipe could also be used to ensure
    # messages are inserted in order, but that would be less efficient.
    func = self._scripts['index_messages']

    arguments = [len(message_ids)] + message_ids
    func(keys=[msgset_key, counter_key], args=arguments)
```

The Lua script then updates the message index using a single<sup><a name="id-2" href="#id-2.ftn">2</a></sup> ZADD call, then increments the side counter:

```lua
-- Read params
local msgset_key = KEYS[1]
local counter_key = KEYS[2]

local num_message_ids = tonumber(ARGV[1])

-- Get next rank value
local rank_counter = tonumber(redis.call('GET', counter_key) or 1)

-- Add ranked message IDs
local zadd_args = {'ZADD', msgset_key}
for i = 0, (num_message_ids - 1) do
    zadd_args[#zadd_args+1] = rank_counter + i
    zadd_args[#zadd_args+1] = ARGV[2 + i]
end

redis.call(unpack(zadd_args))

-- Set next rank value
return redis.call('SET', counter_key, rank_counter + num_message_ids)
```

Since only one Lua script can run at a time, the counter is guaranteed to stay constant while updating the index. Consequently, after the ZADD call, the ordered set is guaranteed to end up with a run of unique rank values for each batch of messages.

So how did it perform? 

I benchmarked both the old and new implementations using zaqar-bench, a simple python+gevent performance testing tool included with Zaqar. I ran the tool with 3,000 producer clients, posting messages to a minimal Zaqar deployment (1 web head running uWSGI and one DB box running a couple of Redis processes).

## Before

Before the patch the results were decent. But, as you can see, some requests  took an inordinate amount of time. High contention for the side counter caused some requests to retry the transaction many times before finally succeeding.

```
req/sec: 5223

ms/req (mean): 3.5 
ms/req (stdev): 7.7 
ms/req (99th): 42.1
ms/req (max): 186.5
```

## After

After applying the Lua patch and re-running the benchmark, the stats not only smoothed out significantly, but throughput jumped by almost 60%. Hooray!

```
req/sec: 8246

ms/req (mean): 2.4
ms/req (stdev): 1.7 
ms/req (99th): 10.7
ms/req (max): 54.6
```

There's still some work to do in order to get those outliers fully under control, but these initial results have me excited to see what else a little Lua love can do.

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup>Larger operations can typically be broken down into smaller ones in order to interleave multiple concurrent requests.
  </li>
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup>This should be faster than multiple ZADD calls, since the Redis code still treats Lua scripts as <em>clients</em>, albeit ones that can bypass the network stack. However, I still need to do an A/B test to see if the difference in performance is significant.
  </li>
</ul>

[1]: https://github.com/andymccurdy/redis-py#lua-scripting
[2]: https://wiki.openstack.org/wiki/Zaqar