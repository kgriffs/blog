---
layout: post.html
title: "Falcon WSGI Framework: 0.1.8"
summary: "Thanks to the hard work of a growing community of contributors, we were able to ship several long-awaited goodies, including request sinks, improved URI decoding, and custom error handlers."
tags: [codez]
---

I'm quite proud of the new Falcon 0.1.8 release. Thanks to our growing community of talented contributors, we were able to ship several long-awaited goodies, including request sinks, improved URI decoding, and custom error handlers.

Also, there was a ton of work done to improve performance in hot code paths, in order to offset the extra processing required by the new features landing in 0.1.8.

## Custom Error Handlers ##

You can now DRY up your error code by registering global handlers. An error handler is just a callable that takes the exception that was raised, plus the standard req and resp args that were passed to the responder, along with the params dict that was passed as kwargs to the responder.

```python
def handle_storage_error(ex, req, resp, params):
    # Log what happened

    # ...

    # Return an appropriate response explictly, or raise an
    # instance of HTTPError as shown here...

    description = ('Sorry, couldn\'t write your thing to the '
                   'database. It worked on my box.')

    raise falcon.HTTPError(falcon.HTTP_725,
                           'Database Error',
                           description)


api = falcon.API()

# If a responder ever raised an instance of StorageError, pass control to
# the given handler.
api.add_error_handler(StorageError, handle_storage_error)

```

Alternatively, you can define a handler on the error class itself. If you name it `handle` then you don't even need to specify the function in `add_error_handler`:

```python
class StorageError(Exception):
    @staticmethod
    def handle(ex, req, resp, params):
        description = ('Sorry, couldn\'t write your thing to the '
                       'database. It worked on my box.')

        raise falcon.HTTPError(falcon.HTTP_725,
                               'Database Error',
                               description)

# ...

# Falcon conveniently assumes the handler is defined as `StorageError.handle`
api.add_error_handler(StorageError)

```

## Request Sinks ##

Request sinks is another handy new feature added in Falcon 0.1.8. What you do is add a regex-based route that slurps up anything that starts with the given pattern. You can make smart proxies with this, or anything else you like.

Here's a ridiculously contrived example that drains any request paths that start
with either '/v1/charts' or '/v1/inventory'.

```python
# Step 1: Define a sink using an extra Proxy thing just for fun
class Proxy(object):
    def forward(self, req):
        return falcon.HTTP_503


class SinkAdapter(object):

    def __init__(self):
        self._proxy = Proxy()

    def __call__(self, req, resp, **kwargs):
        resp.status = self._proxy.forward(req)
        self.kwargs = kwargs


# Step 2: Invoke some magic
app = falcon.API()

sink = SinkAdapter()
app.add_sink(sink, r'/v1/[charts|inventory]')

# Step 3: Profit!

```

## Case-Insensitive Headers ##

Previously, when you set response headers, the header name you used was case-sensitive. This wasn't exactly intuitive in the world of HTTP, where clients and servers are supposed to treat header names as case-insensitive. Among other things, this created an unfortunate gotcha for folks who were trying to proxy requests to a backing service, and selectively overwrite some of the original header values.

Now, when setting headers, their names are normalized to lowercase to avoid this problem. This approach is more performant than using some kind of case-insensitive dict under the covers, and well-behaved clients should be treating response headers they get back from the server as case-insensitive anyway.

That being said, if some of your unit tests were asserting on specific header strings, they may break. If you are using `falcon.testing.StartResponseMock`, you can work around this problem by reading headers via `headers_dict` which is now implemented using a case-insensitive dict class borrowed from the stupendous Requests library.

## Improved URL encoding/decoding ##

Percent-encoded characters in query strings are now properly decoded. Even encoded UTF-8 sequences work like a charm! See also [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt) if you want to know how this is supposed to work and/or you are having trouble falling asleep.

Also, you can now manually encode/decode URI things in your app if you're crazy like that; just `from falcon.util import uri` and you're ready to rock.

## Improved Python 3.3 Performance ##

All WSGI frameworks I've tested slow down when running under Python 3.3, relative to Python 2.7, but thanks to some serious voodoo, Falcon's own performance gap has narrowed quite a bit as of 0.1.8. The difference is now just 12 μs/req. Check out the [latest benchmarks](http://falconframework.org/#Metrics) and see for yourself.

Please, take [0.1.8](https://pypi.python.org/pypi/falcon/0.1.8) for a spin and tell me what you like, what you don't, and what you would like to see in the next version. As always, you can find me on Freenode in **#falconframework** and on Twitter **@kgriffs**.

[Get it while it's hot.](https://pypi.python.org/pypi/falcon)

