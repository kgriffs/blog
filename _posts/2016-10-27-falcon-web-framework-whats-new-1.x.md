---
layout: post.html
title: "Falcon Web Framework: What's New?"
summary: "Version 1.1 of the Falcon WSGI framework is now available, thanks to all the hard work put in by our growing team of awesome contributors. Extra special thanks to everyone who joined us at the PyCon 2015 and 2016 sprints to work on 1.0 and 1.1!"
tags: [code]
---

<img class="right" src="/assets/images/pycon-2016-falcon-web-framework-sprint-1.jpg" width="160px" alt="Falcon web framework sprint at PyCon 2016" />

Earlier this year the Falcon community celebrated the web framework's landmark 1.0 release. It takes a surprising amount of effort to make something simple and elegant, and I want to personally thank the many people who have helped us reach this point through their generous support and contributions to the project over the past few years.

When it comes to web development, there are many options to choose from within the Python community. This is actually a good problem to have, since it gives you a better chance of finding the right tool for the job. We've worked hard to make Falcon a useful, complementary addition to any Python web developer's toolbox. 

Some web developers choose Falcon when the job calls for high performance. For example, they may develop a performance-sensitive microservice in Falcon to complement their Django app. Falcon also works great for developing high-throughput cloud services, microservices, and app backends.

Other web developers choose Falcon when they need low-level control over the way requests are processed. They appreciate how Falcon embraces HTTP instead of paving over it. Falcon makes it easier to reason about the application and to diagnose errors, which is especially helpful in large-scale production deployments.

<img class="left" src="/assets/images/pycon-2016-falcon-web-framework-sprint-3.jpg" width="180px" alt="Falcon web framework sprint at PyCon 2016" />


Finally, web developers choose Falcon due to its clean, well-documented source code. We've worked hard to make it easy to understand the code and to contribute improvements and add-ons. Developers have noted the educational aspects of the Falcon framework; reading its source is a great way to learn more about WSGI, HTTP, Python programming idioms, and performance tuning. 

No tool is perfect, and Falcon is certainly no exception. But the framework has already come a long way and I'm excited to see what the future will bring. If you'd like to help us create that future, please consider [joining the discussion](https://github.com/falconry/falcon/blob/master/CONTRIBUTING.md) and contributing a PR or two. Or, if you've created an add-on please consider listing it [on our wiki](https://github.com/falconry/falcon/wiki/Add-on-Catalog). Thanks!



Recently we released version 1.1 of the Falcon web framework. Many thanks to everyone in the community who contributed to the 1.0 and 1.1 releases! 

Here are some highlights:

## New in Falcon 1.0 

_Please note: For a complete list of changes, including breaking changes and bug fixes, please see the [changelog for version 1.0](http://falcon.readthedocs.io/en/stable/changes/1.0.0.html)_.

### Code of Conduct

A [code of conduct](https://github.com/falconry/falcon/blob/master/CODEOFCONDUCT.md) was added to solidify our community's commitment to sustaining a welcoming, respectful culture. This was not done in response to a specific incident, but rather as a proactive measure to nip any potential problems in the bud as our community grows.

### Routing Improvements

Path segments with multiple field expressions can now be defined at the same level as path segments having only a single field expression. For example, this now works:

```py
api.add_route('/files/{name}', resource_1)
api.add_route('/files/{name}.{ext}', resource_2)
```

Note, however, that using different field names will still cause a conflict:

```py
api.add_route('/files/{id}', resource_1)
api.add_route('/files/{name}/ext', resource_2)  # Raises ValueError
```

Falcon 1.0 also improves support for custom router implementations. `API.add_route()` now accepts additional parameters via `*args`, `**kwargs`. These parameters are passed through to the router's own ``add_route()`` method. Also, `falcon.routing.compile_uri_template()` now supports templates that contain digits and underscores.

### Request and Response Improvements

New `access_route` and `remote_addr` properties were added to the `Request` class for getting upstream IP addresses:

```py
client_ip = req.access_route[0]
last_hop_ip = req.remote_addr
```

The `Response` class was given a `get_header()` method to give apps a way to check if a header has already been set:

```py
request_id = resp.get_header('X-Request-ID')
```

Also, as of Falcon 1.0 both the `Request` and `Response` classes support range header units other than bytes:

```py
# Per RFC 7233, the server must ignore a Range header field
# that contains a range unit that it does not understand.
use_range = (req.range_unit == 'blocks')

# Content-Range: blocks 0-63/64
resp.content_range = (0, 63, 64, 'blocks')
```

### HTTP Error and Status Features

`HTTP_422`, `HTTP_428`, `HTTP_429`, `HTTP_431`, `HTTP_451`, and `HTTP_511` were added to the `falcon` module. We also added three additional error classes, namely `HTTPUnprocessableEntity`, `HTTPTooManyRequests`, and 
`HTTPUnavailableForLegalReasons`. (The fact that some developers need that last one makes me sad, but unfortunately this is the world we live in.)

The `HTTPStatus` class is now available directly under the `falcon` module, and has been properly documented. Furthermore, support for HTTP redirections was added via a set of `HTTPStatus` subclasses to avoid the problem of hooks and responder methods possibly overriding the redirect. Raising an instance of one of these new redirection classes will short-circuit request processing, similar to raising an instance of `HTTPError`.

Also, the default 404 responder now raises an instance of `HTTPError` instead of manipulating the response object directly. This makes it possible to customize the response body using a custom error handler or serializer.

### New Testing Framework

A new testing framework was added that should be more intuitive to use than the old one. The new testing framework performs `wsgiref` validation on all requests. 

```py
from falcon import testing
import myapp


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = myapp.create()


class TestMyApp(MyTestCase):
    def test_get_message(self):
        doc = {u'message': u'Hello world!'}

        result = self.simulate_get('/messages/42')
        self.assertEqual(result.json, doc)
```

Please note that the previous testing framework is now deprecated and will be removed in a future release. Several of Falcon's own tests have been ported to use the new framework, with the remainder to be ported in subsequent releases.

### Breaking Changes in 1.0 

Since 1.0 was a major release, we took the opportunity to clean up a few rough edges. Rather than list all the breaking changes here, I'll just highlight one in particular. 

In 1.0 an option was added to toggle automatic parsing of form params. Falcon will no longer automatically parse, by default, requests that have the content type "application/x-www-form-urlencoded". This was done to avoid unintended side-effects that may arise from consuming the request stream. It also makes it more straightforward for applications to customize and extend the handling of form submissions. Applications that require this functionality must re-enable it explicitly, by setting a new request option that was added for that purpose:


```py
app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
```

A full list of 1.0 breaking changes is included in [the changelog](http://falcon.readthedocs.io/en/stable/changes/1.0.0.html).

## New in Falcon 1.1

_Please note: For a complete list of changes, including bug fixes, please see the [changelog for version 1.1](http://falcon.readthedocs.io/en/stable/changes/1.1.0.html)_.


### Request and Response Improvements
<img class="right" src="/assets/images/pycon-2016-falcon-web-framework-sprint-2.jpg" width="160px" alt="Falcon web framework sprint at PyCon 2016" />

Three new properties were added to the `Request` class. The new `bounded_stream` property can be used in place of the `stream` property to mitigate the blocking behavior of input objects used by some WSGI servers. Also, a `uri_template` property was added to expose the template for the route corresponding to the path requested by the user agent. 

```py
# Load the request body directly into msgpack
resource_representation = msgpack.unpack(req.bounded_stream, encoding='utf-8')

# Log the template that was matched for this request
logger.debug(req.uri_template)
```

In 1.1 we also added an `accept_ranges` property for setting the Accept-Ranges header:

```py
# Tell the client that they should specify ranges in terms of "blocks"
resp.accept_ranges = 'blocks'
```

In addition to the new properties mentioned above, a `context` property was implemented for the `Response` class to mirror the same property that is already available on the `Request` class. In addition, arbitrary custom attributes can now be attached to instances of both `Request` and `Response` as an alternative to adding values to the `context` property or implementing custom subclasses:

```py
# Pass a "customer" resource representation to middleware via the context dict
resp.context['rr'] = customer

# ...or use a custom attribute instead of the context dict
resp.rr = customer

# Also works with Request objects
resp.set_header('X-Request-ID', req.request_id)
```

In other news, when working with query strings, you can now disable CSV-style parsing of query parameter values with the `auto_parse_qs_csv` request option. JSON-encoded query parameter values can now be retrieved and decoded in a single step via `req.get_param_as_dict()`. Also, `req.get_param_as_bool()` now recognizes "on" and "off" in support of IE's default checkbox values. 

### New and Improved Error Classes

In Falcon 1.1 we added two new error classes, `falcon.HTTPUriTooLong` and `falcon.HTTPGone`. All parameters are now optional for most error classes. When no title is specified for an error, it will default to the HTTP status text (e.g., "409 Conflict").

```py
# The target resource is no longer available at the 
# origin server and this condition is likely to be 
# permanent.
raise falcon.HTTPGone()

# All parameters are optional now, but note that you 
# can improve the user experience by specifying some 
# details.
raise HTTPForbidden()
```

### Better Testing

By popular demand, pytest support was added to Falcon's testing framework:

```py
from falcon import testing
import pytest

import myapp


@pytest.fixture(scope='module')
def client():
    # Assume the hypothetical `myapp` package has a
    # function called `create()` to initialize and
    # return a `falcon.API` instance.
    return testing.TestClient(myapp.create())


def test_get_message(client):
    doc = {u'message': u'Hello world!'}

    result = client.simulate_get('/messages/42')
    assert result.json == doc
```

Regardless of whether you use unittest or pytest, when simulating a request using Falcon's testing framework, query string parameters can now be specified as a `dict`, as an alternative to passing a raw query string.

Also, the `falcon.testing.Cookie` class was added to represent a cookie returned by a simulated request; `falcon.testing.Result` now exposes a `cookies` attribute for examining returned cookies. 

### Middleware Processing

Falcon's middleware processing logic was revamped to improve performance and to fix a couple of edge cases.

In addition, a `req_succeeded` flag is now passed to the `process_request()` middleware method to signal whether or not an exception was raised while processing the request:

```py
class ExampleMiddleware(object):
    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            # ...
        else:
            # ...
```

Per our policy of not introducing breaking changes in point releases (not to mention never introducing undocumented breaking changes that can take you by surprise), we added shimming logic to avoid breaking existing middleware methods that do not yet accept this new parameter.

### Other Goodies

A new CLI utility, `falcon-print-routes`, was added that takes in a `module:callable`, introspects the routes, and prints the results to `stdout`. This utility is automatically installed along with the framework:

```bash
    $ falcon-print-routes commissaire:api
    -> /api/v0/status
    -> /api/v0/cluster/{name}
    -> /api/v0/cluster/{name}/hosts
    -> /api/v0/cluster/{name}/hosts/{address}
```

Finally, `falcon.get_http_status()` was implemented to provide a way for apps to look up a full HTTP status line, given just a status code.

```py
status = falcon.get_http_status(719)
```

Thanks again to all of our awesome contributors who have made these releases possible!

@kgriffs
