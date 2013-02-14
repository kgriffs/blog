Outline

* Overview
* Does the world really need another Python web framework?
* How is Falcon different?
* What's on the roadmap?
* What does a Falcon-based web service look like?
* Where can I go to learn more?
* How can I get involved?
* Summary

When it comes to web services, latency and efficiency matters. The last thing you want is your web framework to bottleneck you API. Previously, I shared some performance testing results involving a queuing message service using a custom web micro-framework, Rawr. Several of you asked about getting the code for Rawr, and so I'm happy to announce that it's successor has been open-sourced courtesy of Rackspace. 

Falcon is a new, [high-performance framework][home] for building web services and cloud APIs. It's WSGI-based, and works great with Python 2.7, Python 3.3, and PyPy, giving you a wide variety of deployment options. While [the project][source] is still quite young (v0.1.1 at the time of this writing), it's far enough along to be useful in real applications. In fact, we are already using it for a couple of projects at Rackspace.

[home]: http://falconframework.org
[source]: https://github.com/racker/falcon

## Does the world need another Python web framework? ##

I didn't want to write Falcon. It would have been far easier to take something off the shelf and plug it in. However, a few things pushed me over the edge:

* The poor performance of most web frameworks under load. At high concurrency rates, with async socket IO, API servers become CPU-bound. When that happens, even a small decrease in the number of CPU cycles needed to service each request results in a dramatic *increase* in throughput, as well as a significant reduction in latency.
* Most web frameworks come with a lot of baggage that is great if you are developing a web app, but useless when building web APIs. In fact, such frameworks only complicate deployment, and incease your risk of security vulnerabilities.
* Some Python web frameworks come with their own async library, or are tightly coupled to a third-party library such as Twisted. This limits which Python flavors you can run, and prevents you from using the async library of your choice.

## How is Falcon different? ##

First, Falcon is fast. [Really fast][bench]. It's no coincidence the framework shares the genus name of the [fastest animal on Earth][peregrine].  

Second, Falcon doesn't try to do everything; the web framework is specifically targeted at web API development. That means very few dependencies, and no HTML-specific cruft. What Falcon *does* do is encourage idiomatic HTTP API design (without being too pedantic).

Third, Falcon avoids system-level dependencies. In addition to reducing the framework's attack surface, and giving you the freedom to choose your own I/O library, keeping Falcon high-level means that it's a snap to use the web framework on various Python flavors, including Python 2.7, PyPy, and Python 3.3. 

[bench]: http://falconframework.org/#Metrics
[peregrine]: https://en.wikipedia.org/wiki/Peregrine_Falcon

## What does a Falcon-based web service look like? ##

## What's next for the framework? ##

-docs
-etc.

## How can you get involved? ##

-- try it out, issues list, pull requests, etc.
-- docs
-- also summary
