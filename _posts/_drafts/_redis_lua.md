---
layout: post.html
title: 
summary: 
tags: [code]
id: DDDB4122-3744-4E3D-893B-341686C154D4
---

Lately I've been working on Zaqar's new Redis driver. Zaqar provides a stateless REST API for creating and consuming message feeds. When you have multiple observers of a feed, each observer keeps track of its own position in the feed using a marker. 

In this design, there is an unfortunate race condition that emerges as a result of the interplay betweem the message producers and observers.

[talk about it, possibly use tutorial]

The way we originally dealt with this in the Redis driver was to use the server's support for transactions. To do this with Redis, you set a watch on a key (or set of keys) upon which the transaction depends, then prepare the transaction by creating a pipeline of commands, and finally attempt to execute the pipeline. An error will be raised if any of the watched keys have changed in the meantime, causing all commands to abort. 

Here is a simplified version of the code in Zaqar that we originally used to post messages.

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

As you can see, Zaqar uses an ordered set to index messages. It ranks the messages using a so-called "rank counter", which is nothing more than a side counter that is stored alongside the other data. In order to return to the client a list of messages *after* a given "marker" (which is actually just a message ID), the service looks up the rank of the specified message ID and proceeds to list all the following messages (in rank order).

This works, but the more concurrent requests served, the more frequent the counter collisions. The result is a lot of wasted time retrying the operation, and significantly higher latency. Fortunately, there is a better way.

Since version 2.6, Redis supports server-side execution of Lua scripts. In some ways this is similar to the notion of "stored procedures" in the RDBMS world. However, only one Redis script may run at a time, and no other commands may run concurrently. In this way you can execute a batch of commands atomically, without having to use "watch-abort-retry" loops in the client. On the other hand, it also means scripts must finish quickly to avoid starving other incoming commands. 

By moving much of the logic to Lua, we were able to greatly simplify the Python code:

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

And here is the lua script:

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

Since only one Lua script can run at a time, the counter will not change out from under us. Consequently, after the ZADD call, the ordered set is guaranteed to end up with a run of unique rank values for each batch of messages.

  So how did it perform?

I benchmarked with 3000 producer clients against a zaqar deployment with 1 web head and messages sharded across two redis processes, both colocated but on a separate box from the web head. The difference in performance was remarkable:

[before]

[after]

Not too shabby. I think we should look for other places in the driver that could benefit from a little Lua love.

Lua lets you extend the out-of-the-box semantics of Redis to provide more sophisticated operations. indexeing, etc. In a sense, it lets you create your own, domain-specific database server.

check out rackspace's new thing.

[add references to redis lua scripting, zaqar - is pretty new, lots to do, contributors welcome, etc.]

@kgriffs

