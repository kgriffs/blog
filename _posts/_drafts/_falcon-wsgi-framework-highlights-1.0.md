---
layout: post.html
title: "Falcon WSGI Framework: 1.0"
summary: "Version 1.0.0 of the Falcon WSGI framework is now available, thanks to all the hard work put in by our growing team of awesome contributors. Extra special thanks to everyone who joined us at the PyCon 2015 sprint in Montreal!"
tags: [code]
---

{image}

The Falcon community recently celebrated the web framework's landmark 1.0 release. It takes a suprising amount of effort to make something simple and elegant, and I want to personally thank the many people who have helped us reach this point through their generous support and contributions to the project over the past few years.

When it comes to web development, there are many options to choose from within the Python community. This is actually a good problem to have, since it gives you a better chance of finding the right tool for the job. We've worked hard to make Falcon a useful, complementary addition to the Python web developer's toolbox. 

Some web developers choose Falcon when the job calls for high performance. For example, they may develop a performance-sensitive microservice in Falcon to complement their Django app. Falcon also works great for developing high-throughput cloud services and app backends.

Other web developers choose Falcon when they need low-level control of the way requests are processed. They appreciate how Falcon embraces HTTP, rather than paves over it. Falcon makes it easier to reason about the application and to diagnose errors. This is especially helpful in large-scale production deployments.

{testimonials for each}

Finally, web developers choose Falcon due to its clean, well-documented source code. We've worked hard to make it easy to understand the code and contribute improvements and add-ons. Also, developers have noted the educational aspects of the Falcon framework; reading its source is a great way to learn more about WSGI, HTTP, Python programming idioms, and performance tuning. 

No tool is perfect, and Falcon is certainly no exception. But the framework has already come a long way and I'm excited to see what the future will bring.

## New in Falcon 1.0 

A [code of conduct](https://github.com/falconry/falcon/blob/master/CODEOFCONDUCT.md) was added to solidify our community's commitment to sustaining a welcoming, respectful culture. This was not done in response to a specific incident, but rather as a proactive measure to nip any potential problems in the bud as our community grows.

In terms of functionality, we added support for several additional error statuses. HTTP\_422, HTTP\_428, HTTP\_429, HTTP\_431, HTTP\_451, and HTTP\_511 were added to the `falcon` module. We also added three additional error classes, namely `HTTPUnprocessableEntity`, `HTTPTooManyRequests`, and 
`HTTPUnavailableForLegalReasons`. The fact that some developers need that last one makes me sad, but unfortunately this is the world we live in.



- CPython 3.5 is now fully supported.
- The `HTTPStatus` class is now available directly under the falcon
  module, and has been properly documented.
- Support for HTTP redirections was added via a set of
  `HTTPStatus` subclasses. This should avoid the problem of hooks and
  responder methods possibly overriding the redirect. Raising an
  instance of one of these new redirection classes will short-circuit
  request processing, similar to raising an instance of `HTTPError`.
- The default 404 responder now raises an instance of `HTTPError`
  instead of manipulating the response object directly. This makes it
  possible to customize the response body using a custom error handler
  or serializer.
- A new method, `get_header()`, was added to the `Response` class.
  Previously there was no way to check if a header had been set. The
  new `get_header()` method facilitates this and other use cases.
- `Request.client_accepts_msgpack` now recognizes
  "application/msgpack", in addition to "application/x-msgpack".
- New `access_route` and `remote_addr` properties were added to the
  `Request` class for getting upstream IP addresses.
- The `Request` and `Response` classes now support range units other
  than bytes.
- The `API` and `StartResponseMock` class types can now be customized
  by inheriting from falcon.testing.TestBase and overriding the
  `api_class` and `srmock_class` class attributes.
- Path segments with multiple field expressions may now be defined at
  the same level as path segments having only a single
  field expression. For example:

      api.add_route('/files/{file_id}', resource_1)
      api.add_route('/files/{file_id}.{ext}', resource_2)

- Support was added to `API.add_route()` for passing through
  additional args and kwargs to custom routers.
- Digits and the underscore character are now allowed in the
  `falcon.routing.compile_uri_template()` helper, for use in custom
  router implementations.
- A new testing framework was added that should be more intuitive to
  use than the old one. Several of Falcon's own tests were ported to
  use the new framework (the remainder to be ported in a
  subsequent release.) The new testing framework performs wsgiref
  validation on all requests.
- The performance of setting `Response.content_range` was improved
  by \~50%.
- A new param, `obs_date`, was added to
  `falcon.Request.get_header_as_datetime()`, and defaults to `False`.
  This improves the method's performance when obsolete date formats do
  not need to be supported.


## Breaking changes in Falcon 1.0

## Fixes in Falcon 1.0


---

1.1 ?







So what's new in Falcon 1.0?

## New Router

Thanks to [Richard Olsson][1] we now have a new engine that compiles routes into a decision tree. This improves lookup performance for large APIs, and will also allow us to more efficiently implement some new URI template features. As part of this work, we also made it easier to use [custom routing engines][routing].

<img class="right" src="/assets/images/linear-router.png" alt="Falcon web framework linear routing engine" width="395" height="305" />

In version 0.2, Falcon's default router compiles each URI template to a regular expression. For each incoming request, Falcon iterates through this list of regexes, attempting to match each one, in turn, against the requested path. This means that the order in which routes are added can make a big difference in performance; when a path is requested for a route toward the back of the list, a bunch of regex match operations must be attempted before finding the correct route.

The new engine, by contrast, takes a divide-and-conquer approach to match a given request path to a resource. This works well because developers tend to organize APIs hierarchically. Richard and I started with a couple of prototypes that implemented a generic routing engine. This engine traversed a tree of nodes, with each node representing a single path segment in the URL namespace.

<img class="left" src="/assets/images/tree-router.png" alt="Falcon web framework tree-based routing engine" width="278" height="235" />

We found that the most efficient of the two prototypes ran slightly faster when looking up a long path with multiple segments. It wasn't quite as fast for a simple path, but was still competitive. The order in which routes were added to the regex-based router also made a big difference; when looking up a route that was defined later in the router's search list, the prototype's divide-and-conquer approach easily won out.

<div style="clear:both"></div>

The final engine incorporated into Falcon 0.3 takes this strategy one step further. It generates a static decision tree, rather than running a generic traversal algorithm over an abstract tree. The generated code looks something like this:

```python
def find(path, return_values, expressions, params):
    path_len = len(path)
    if path_len > 0:
        if path[0] == "parks":
            if path_len > 1:
                params["park_id"] = path[1]
                if path_len > 2:
                    if path[2] == "map":
                        if path_len == 3:
                            return return_values[11]
                        return None
                    return None
                if path_len == 2:
                    return return_values[10]
                return None
            return None
        if path[0] == "libraries":
            
            # ...

```

This provides an extra boost of performance by avoiding looping constructs and dict lookups. It's especially fast when JITed under PyPy.

## New URI Template Feature

Also thanks to [Richard Olsson][1], URI templates can now include multiple parameterized fields within a single path segment. For example, you might use this template to route a GH-style request:

```
/repos/{org}/{repo}/compare/{usr0}:{branch0}...{usr1}:{branch1}
```

Our new engine paves the way for implementing some other, long-overdue templating features as well. Stay tuned!

## Cookie Support

Thanks to the tireless efforts of [Henrik Tudborg][2], we now have support for reading and writing cookies. A cookie can be read from the request via the new `cookies` property, which returns a simple `dict`:

```python
cookies = req.cookies
my_cookie_value = cookies['my_cookie']
```

You can also set cookies on a response with the new `set_cookie` method:

```python
resp.set_cookie("my_cookie", "my cookie value",
                max_age=600, domain="example.com")
```

See also: http://falcon.readthedocs.org/en/0.3.0/api/cookies.html

## Jython 2.7 support

During the PyCon 2015 sprint, [Clara Bennett][3] added support to Falcon for Jython 2.7. Now you can use Falcon along with [Clamp and Fireside][hellowsgi] (or ModJy) to create JVM-friendly web services in Python!

## Other goodies

* The Request class gained a new helper, `get_param_as_date(...)`, for getting a query param as a date.
* Date header values are now returned as `datetime` objects, rather than raw string.
* Friendly constants for status codes were added, so that you can now say `falcon.HTTP_NO_CONTENT` instead of `falcon.HTTP_204`.
* Query string parsing was made much more robust when decoding embedded documents, such as JSON.

See also the [changelog on RTD][changelog].

[1]: https://github.com/richardolsson
[2]: https://github.com/tbug
[3]: https://github.com/csojinb

[routing]: http://falcon.readthedocs.org/en/0.3.0/api/routing.html
[changelog]: http://falcon.readthedocs.org/en/0.3.0/changes/0.3.0.html
[hellowsgi]: https://github.com/jimbaker/hellowsgi
