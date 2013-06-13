
When measuring the performance of a web service, I like to find out how quickly the service responds to requests (latency), and how much horsepower is required to serve those requests (efficiency). Efficiency is important because it allows me to serve large numbers of customers at a reasonable cost (both to them and to myself). Latency is also important to me, because it often correlates with usability; if an API responds faster, then the app that is using that API responds faster, and by extension the person using that app is happier and more likely to spend more time with that app. On the other hand,

Of course, there are many factors that influence web service latency and efficiency; one area that often gets overlooked or glossed over is the performance of your web framework. Previously, I shared some performance testing results involving a queuing message service using a custom web micro-framework, Rawr. Those results made it clear that even a small improvement in performance of the framework (in the case of Rawr, compiling it with Cython) can make a big difference in performance.

Several of you asked about getting the code for Rawr, and so I'm happy to announce that it's successor, Falcon, has been open-sourced, courtesy of your friendly neighborhood Rackspace. If nothing else, I hope contributing this framework to the community will raise the bar on Python web framework performance, providing a laboratory of sorts for experimentation in this space.

Falcon is a new, [high-performance framework][home] for building web services and cloud APIs. It's WSGI-based, and works great with Python 2.6, Python 2.7, Python 3.3, and PyPy, giving you a wide variety of deployment options. While [the project][source] is still quite young (v0.1.6 at the time of this writing), it's far enough along to be useful in real applications. In fact, we are already using it for a few cloud projects at Rackspace.

[home]: http://falconframework.org
[source]: https://github.com/racker/falcon

## Does the world need another Python web framework? ##

>>> reinvent...all the things!

I didn't particularly *want* to write Falcon. It would have been far easier to take something off the shelf and just plug it in. However, a few things pushed me over the edge:

* The poor performance of most web frameworks under load. At high concurrency rates, with async socket IO, API servers can become CPU-bound. When that happens, every microsecond counts; reducing the cost to service a single request by just 1 us makes a huge difference in terms of throughput and latency.
* Most web frameworks come with a lot of HTML-centric tooling that is fantastic if you are developing a web app, but quite useless when building an API. All those unused modules and dependencies simply sit around, consuming RAM, increasing your risk of security vulnerabilities, and complicating deployment.
* Many frameworks try too hard, in my opinion, to abstract away what's going on under the hood, making it difficult to reason about (and tune) the flow of HTTP in and out of your API. Magic is wonderful at development time, but a nightmare when it comes time to debugging production issues.

I think the world *does* need another Python web framework, if for no other reason than to raise awareness of these issues and get the community thinking about ways to overcome them.

## How is Falcon different? ##

First, Falcon is already [pretty fast][bench], and will be getting faster. It's no coincidence the framework shares the genus name of the [fastest animal on Earth][peregrine]. When there is a conflict between saving the developer a few keystrokes and saving a few microseconds to serve a request, Falcon is strongly biased toward the latter.

Second, Falcon is lean. It doesn't try to be everything to everyone, focusing instead on a single use case: HTTP APIs. Falcon doesn't include a template engine, form helpers, or an ORM. The only dependency Falcon takes is on Six, the Python 2 and 3 compatibility library. Bring your own async library, your own serializer, your own DAL, your own...whatever.

Third, Falcon eschews magic. When you use the framework, it's pretty obvious which inputs lead to which outputs. Also, it's blatantly obvious where variables originate. All this makes it easier for you and your posterity to reason about your code, even months (or years) after you wrote it.

[bench]: http://falconframework.org/#Metrics
[peregrine]: https://en.wikipedia.org/wiki/Peregrine_Falcon

## When would you not use Falcon? ##

A few things to consider:

**Reuse.** If you constantly go back and forth between web app and API development, you may want to choose a less specialized framework than Falcon, so you don't have to context-switch between two different interfaces all day long. That being said, many apps these days serve static assets and render everything in JS, in which case Falcon could be a nice way to build your backing API.

**Features.** This is a low-level framework, which gives you a lot of freedom, but also requires a little more elbow grease. If you just want to make a quick website or app, you'll want something with more bells and whistles, such as Django, Pecan, or Flask.

**Maturity.** Falcon is still a young project and not as battle-tested as some other frameworks out there. Caveat emptor.

**Tuning.** Most projects don't have aggressive performance, utilization, and/or security requirements. If you find that you are more productive using a different framework, go ahead and use it! I won't cry. At least, not when anyone is looking...

## What does a Falcon-based web service look like? ##

Here is a simple example from Falcon's README, showing how to get starting writing an API:

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

### More Cowbell ###

Here is a more involved example, demonstrating getting headers and query parameters, handling errors, and reading/writing message bodies.

```python

import json
import logging

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
    if not req.client_accepts_json():
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

            raise falcon.HTTPServiceUnavailable('Service Outage', description)

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

```

## What's next for the framework? ##

Roadmap
-docs
-hooks
-etc.

## How can you get involved? ##

-- try it out, issues list, pull requests, etc.
-- docs
