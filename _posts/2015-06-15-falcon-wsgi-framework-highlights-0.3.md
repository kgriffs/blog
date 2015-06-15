---
layout: post.html
title: "Falcon WSGI Framework: 0.3.0"
summary: "Version 0.3 of the Falcon WSGI framework is now available, thanks to all the hard work put in by our growing team of stylish and talented contributors. Extra special thanks to everyone who joined us at the PyCon 2015 sprint in Montreal!"
tags: [code]
---

<img class="left" src="/assets/images/falcon-sprint-pycon-2015.JPG" alt="Falcon web framework - PyCon 2015 sprint" width="100" height="75" />

Version 0.3 of the Falcon WSGI framework is now available, thanks to all the hard work put in by our growing team of stylish and talented contributors. Extra special thanks to everyone who joined us at the PyCon 2015 sprint in Montreal!

So what's new in Falcon 0.3?

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

This provides an extra boost of performance by avoiding looping constructs and dict lookups. There are still a few minor performance optimizations that could be made It's especially fast when JITed under PyPy.

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