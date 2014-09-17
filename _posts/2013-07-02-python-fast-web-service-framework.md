---
layout: post.html
title: "An Unladen Web Framework"
summary: Falcon is a new web framework for building efficient cloud APIs and stirring up controversy.
tags: [code]
id: f254b484-e367-11e2-b38b-6a9145c3e185
---

When measuring the performance of a web service, I like to find out how quickly the service responds to requests (latency), and how much horsepower is required to serve each request (efficiency).

Efficiency is important because it allows me to serve large numbers of customers at a reasonable cost (both to them and to myself). Latency is also important to me, because it correlates with usability; if an API responds faster, then apps using that API respond faster, and by extension the people using
<img class="left" src="/assets/images/web-framework-performance.gif" width="240px" height="127px" alt="Web Framework Performance: Latency and Efficiency" /> those apps are happier, and more likely to spend more time with those apps. Yay!

Of course, there are many factors that influence web service latency and efficiency; one area that often gets overlooked or downplayed is the performance of the underlying web framework. Previously, I shared some performance testing results involving a queuing message service that used Rawr, a proprietary micro-framework I developed for Rackspace a few years back. Those results made it clear that even a small improvement in performance of the framework (in the case of Rawr, compiling it with Cython) can make a big difference in performance.

Several of you asked about getting the code for Rawr, and so I'm happy to announce that it's successor, Falcon, has been open-sourced, courtesy of your friendly neighborhood Rackspace. If nothing else, I hope contributing this framework to the community will raise the bar on Python web framework performance, providing a laboratory of sorts for experimentation in this space.

## Introducing the Falcon Web Framework ##

<img src="/assets/images/falcon-no-perch.png" width="159px" height="176px" alt="Falcon image courtesy of John O'Neill." />


[Falcon][home] is a new, high-performance web framework for building web services and cloud APIs with Python. It's WSGI-based, and works great with Python 2.6, Python 2.7, Python 3.3, and PyPy, giving you a wide variety of deployment options. While [the project][source] is still quite young (v0.1.6 at the time of this writing), it's far enough along to be useful in real applications. In fact, we're already trying it out in a few cloud projects at Rackspace.

[home]: http://falconframework.org
[source]: https://github.com/racker/falcon

## Yet Another Web Framework ##

I didn't particularly *want* to write Falcon. It would have been far easier to take something off the shelf and just plug it in. However, a few things pushed me over the edge:

* Python web frameworks often perform rather poorly under load. At high concurrency, using async IO, API servers can become CPU-bound. When that happens, every microsecond counts. I wondered if I could make something that could perform a little better than your average framework.
* Most web frameworks come with a lot of HTML-centric tooling that is fantastic if you are developing a web app, but quite useless for building an API. In that case, all they do is waste RAM, increase your chance of a security exploit, and generally make a nuisance of themselves.
* Many frameworks try too hard, in my opinion, to abstract away what's going on under the hood, making it difficult to reason about the river of HTTP flowing in and out of your API. Magic is wonderful at development time, but a nightmare when it comes time to debug a hairy production issue.

## How is Falcon different? ##

First, Falcon is already [pretty fast][bench], and will be getting faster. When there is a conflict between saving the developer a few keystrokes and saving a few microseconds to serve a request, Falcon is strongly biased toward the latter.


Second, Falcon is lean. It doesn't try to be everything to everyone, focusing instead on a single use case: HTTP APIs. Falcon doesn't include a template engine, form helpers, or an ORM. When you sit down to write a web service with Falcon, you choose your own adventure in terms of async I/O, serialization, data access, etc. In fact, the only dependency Falcon takes is on Six, to make it easier to support both Python 2 and 3.

<img class="block" src="/assets/images/flight-silhouettes.gif" width="580px" alt="Falcon image courtesy of L. Shyamal and Wikipedia." />

Third, Falcon eschews magic. When you use the framework, it's pretty obvious which inputs lead to which outputs. Also, it's blatantly obvious where variables originate. All this makes it easier for you and your posterity to reason about your code, even months (or years) after you wrote it.

[bench]: http://falconframework.org/#Metrics

## When would you use Falcon? ##

I'm not going to pretend that Falcon is the best choice for all projects, or even the majority of them. Here are a few things to consider when choosing a web framework for your next project:

**Reuse.** If you constantly go back and forth between web app and API development, you may want to choose a less-specialized framework than Falcon, so you don't have to context-switch between two different environments all day long. That being said, many apps these days serve static assets and render everything in JS, in which case Falcon could be a nice way to build the backing API.

**Features.** Falcon is a low-level framework, which gives you a lot of freedom, but also requires a little more elbow grease. If you just want to make a quick website or app, you might consider something with more bells and whistles than Falcon (e.g., Django, Pecan, or Flask)

**Maturity.** Falcon is still a young project and not as battle-tested as some other frameworks out there. Caveat emptor.

## What does a Falcon-based web service look like? ##

Here is a simple example from Falcon's README, showing how to get started writing an API:

```python
# things.py

# Let's get this party started
import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')

# falcon.API instances are callable WSGI apps
app = api = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
api.add_route('/things', things)

```

You can run the above example using any WSGI server, such as uWSGI
or Gunicorn. For example:

```bash
$ pip install gunicorn
$ gunicorn things:app
```

Then, in another terminal:

```bash
$ curl localhost:8000/things
```

Here is a more involved example that demonstrates reading headers and query parameters, handling errors, and working with request and response bodies.

```python

import json
import logging
from wsgiref import simple_server

import falcon


class StorageEngine:
    pass


class StorageError(Exception):
    pass


def token_is_valid(token, user_id):
    return True  # Suuuuuure it's valid...


def auth(req, resp, params):
    # Alternatively, do this in middleware
    token = req.get_header('X-Auth-Token')

    if token is None:
        raise falcon.HTTPUnauthorized('Auth token required',
                                      'Please provide an auth token '
                                      'as part of the request',
                                      'http://docs.example.com/auth')

    if not token_is_valid(token, params['user_id']):
        raise falcon.HTTPUnauthorized('Authentication required',
                                      'The provided auth token is '
                                      'not valid. Please request a '
                                      'new token and try again.',
                                      'http://docs.example.com/auth')


def check_media_type(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPUnsupportedMediaType(
            'Media Type not Supported',
            'This API only supports the JSON media type.',
            'http://docs.examples.com/api/json')


class ThingsResource:

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('thingsapi.' + __name__)

    def on_get(self, req, resp, user_id):
        marker = req.get_param('marker') or ''
        limit = req.get_param_as_int('limit') or 50

        try:
            result = self.db.get_things(marker, limit)
        except Exception as ex:
            self.logger.error(ex)

            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
              'Service Outage',
              description,
              30)

        resp.set_header('X-Powered-By', 'Donuts')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)

    def on_post(self, req, resp, user_id):
        try:
            raw_json = req.stream.read()
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_748,
                                   'Read Error',
                                   'Could not read the request body. Must be '
                                   'them ponies again.')

        try:
            thing = json.loads(raw_json, 'utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        try:
            proper_thing = self.db.add_thing(thing)

        except StorageError:
            raise falcon.HTTPError(falcon.HTTP_725,
                                   'Database Error',
                                   "Sorry, couldn't write your thing to the "
                                   'database. It worked on my machine.')

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing.id)

wsgi_app = api = falcon.API(before=[auth, check_media_type])

db = StorageEngine()
things = ThingsResource(db)
api.add_route('/{user_id}/things', things)

app = application = api

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
  httpd = simple_server.make_server('127.0.0.1', 8000, app)
  httpd.serve_forever()

```

## What's next? ##

I need your help! Take Falcon for a test drive and tell me what you think.

**Get Involved!**

* Contribute [some docs][docs_issue] and/or write a blog post
* Improve the router's support of [URI templates][uri_templates]
* Create an [optimized alternative][urllib_issue] to urllib.quote
* Add more [scenarios][bench_issue] and frameworks to the benchmarking suite
* Or choose your own [adventure][milestones]


[docs_issue]: https://github.com/racker/falcon/issues/15
[urllib_issue]: https://github.com/racker/falcon/issues/134
[bench_issue]: https://github.com/racker/falcon/issues/151
[uri_templates]: https://github.com/racker/falcon/issues/35
[milestones]: https://github.com/racker/falcon/issues/milestones
