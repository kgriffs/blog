---
layout: post.html
title: Stand back... I'm going to try science!
summary: Check out these results from a round of rigorous performance testing comparing Python, PyPy and Node.js 
tags: [performance]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

The majority of benchmarks posted on the web are derived from testing simple "hello world" apps. Although certainly better than nothing, these tests tell us little about real-world performance. Ideally, one would compare multiple implementations of a non-trivial application, but this takes a lot of time that is often hard to justify in the face of dogged competition and looming deadlines. Occasionally, however, the stars *do* align, and one has the chance to conduct such an experiment.

Lately, I've been researching the various merits of Python vs. JavaScript (ala Node.js), in terms of developing web-scale cloud services. In the course of my work, I ported an internal HTTP-based event queuing service from Python (currently running in production) to JavaScript. In a [previous post][last-post], I shared the results from some informal performance testing of these implementations.  

In this post, I'd like to share my results from a second round of more rigorous performance testing, during which the test environment and variables were tightly controlled<sup><a name="id-1" href="#id-1.ftn">1</a></sup>. I switched from [ApacheBench][ab] to [Autobench][autobench]/[Httperf][httperf], in order to generate a more consistent, realistic load. I also [monkey-patched PyMongo][pymongo-gevent] this time around, so that both Python and Node implementations would use non-blocking I/O all the way through.

[last-post]: /2012/10/23/python-vs-node-vs-pypy.html
[autobench]: http://www.xenoclast.org/autobench/
[httperf]: http://www.hpl.hp.com/research/linux/httperf/
[ab]: https://en.wikipedia.org/wiki/ApacheBench
[pymongo-gevent]: http://api.mongodb.org/python/current/examples/gevent.html

## Testing Environment ##

*Servers*

* [Rackspace Cloud](http://www.rackspace.com/cloud/public/servers/techdetails/) Virtual Machines
  * 4GB RAM
  * 2 vCPUs
  * Next Generation Platform
  * Chicago Region (ORD)
* Arch Linux (2012.08) 
  * x86_64
  * Full system upgrade (pacman -Syu)
  * linux-3.6.5-1
* Tuning
  * Set nofile to 10000 in /etc/security/limits.conf
  * Updated [/etc/sysctl.conf](https://gist.github.com/4027835) to handle a large number of TCP requests and socket churn

*Network*

* 200 Mbps, per server
* Internal network interface (10.x.x.x)

*Python*

* CPython 2.7.3
* PyPy 1.9.0 
* Gevent 1.0rc1
* PyMongo 2.3
* WebOb 1.2.3

*Node.js*

* Node.js 0.8.14
* Connect 2.5.0
* node-mongodb-native 1.1.11

*Other*

* MongoDB 2.2
* Autobench 2.1.2
* Httperf 0.9.0 ([recompiled][httperf-recompiled])

[httperf-recompiled]: http://gom-jabbar.org/articles/2009/02/04/httperf-and-file-descriptors

## Actors ##

*Cloud Servers*

* 3 Autobench hosts
* 1 API server
* 1 DB server 

*Implementations*

* **Node.js**: V8 + Node.js + Connect
* **Gevent**: CPython + [gevent.wsgi][gevent-wsgi] + [gevent.monkey.patch_all()][patch-all]
* **WsgiRef**: CPython + WSGI Reference Implementation
* **WsgiRef-PyPy**: PyPy + WSGI Reference Implementation

[gevent-wsgi]: http://www.gevent.org/gevent.wsgi.html
[patch-all]: http://www.gevent.org/gevent.monkey.html

## Benchmarks ##

As in my previous experiment, I benchmarked retrieving a fixed set of events from an event queuing service backed by MongoDB, with alternative service implementations in Python and JavaScript. Unfortunately, I was not able to directly compare PyPy to both CPython *and* Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the queuing service a third time (using a non-blocking framework that works with PyPy, such as Tornado).

---

*<strong>Update:</strong> See my followup post on [Tornado, Gevent, PyPy and Cython][redux], in which I share my results from running my app with Tornado on PyPy.*

---

For each test, I ran Autobench directly against a single message bus implementation. I set *min\_rate* and *max\_rate* to 20 and 2000, respectively, in order to test a wide range of requests per second<sup><a name="id-2" href="#id-2.ftn">2</a></sup>. The x axes on the graphs below represent the range of req/sec attempted.

I carried out all benchmarks against a single instance of each implementation; no clustering or load balancing solutions were employed (i.e., HAProxy, Gunicorn, Node's *Cluster* module, etc.). Although this setup does not model production deployments, it removes variability in the results, making them easier to verify and interpret.

For those implementations that supported HTTP/1.1 Keep-Alive<sup><a name="id-3" href="#id-3.ftn">3</a></sup>, I ran each test twice, once with 1 GET<sup><a name="id-4" href="#id-4.ftn">4</a></sup> per connection, and once again with 10 GETs per connection. I denoted this in the results by appending the number of requests per connection to each implementation name, as in *Gevent (1)* and *Gevent (10)*. The results of the latter test may be especially instructive regarding web apps, since browsers typically perform several requests per connection.

Each request to the message bus returned an identical set of JSON-encoded events (shallow objects, ~1K of text). I also tested *Gevent (10)* and *Node.js (10)* against a larger result set containing ~64K of events, and against an empty result set (where the server responded to every request with *204 No Content*). 

[redux]: /2012/12/12/gevent-vs-tornado-benchmarks.html

## Results ##

Except where noted, only the results from testing the 1K data set appear in the graphs below. I used [Flot][flot] to visualize the raw data (see also the <a type="text/javascript" download="" href="/assets/js/python-vs-node-vs-pypy-benchmarks.js">JavaScript file</a> accompanying this post).

Now, I'll step aside for a moment and let the data speak for itself...

[flot]: http://www.flotcharts.org/

## Gevent vs. Node.js ##

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation (req/sec)
<div id="graph-1-stdev" class="flot"></div>

## Sync vs. Async ##

Throughput (req/sec)
<div id="graph-5-rps" class="flot"></div>

Response Time (ms)
<div id="graph-5-rt" class="flot"></div>

Errors
<div id="graph-5-errors" class="flot"></div>

## PyPy vs. CPython ##

Throughput (req/sec)
<div id="graph-4-rps" class="flot"></div>

Response Time (ms)
<div id="graph-4-rt" class="flot"></div>

Errors
<div id="graph-4-errors" class="flot"></div>

## 0 KiB vs. 1 KiB vs. 64 KiB ##

Throughput (req/sec)
<div id="graph-2-rps" class="flot"></div>

Response Time (ms)
<div id="graph-2-rt" class="flot"></div>

Errors
<div id="graph-2-errors" class="flot"></div>

Standard Deviation (req/sec)
<div id="graph-2-stdev" class="flot"></div>

## Q.E.D. ##

Node.js outperforms Gevent significantly in terms of latency and error rates for small data transfers (~1K). However, in the case of larger response bodies (~64K), the difference between the two platforms is more subtle. Overall, the best-case scenario for Node.js appears to be serving large numbers of concurrent requests for small chunks of data, over a persistent connection.

PyPy performs only slightly better than CPython when using Python's WSGI reference implementation. More work is needed to determine whether PyPy would perform similarly to Node.js given a compatible, non-blocking Python web framework *and* a non-blocking MongoDB driver.

Finally, regarding blocking vs. non-blocking I/O frameworks, Gevent certainly outperforms WsgiRef in terms of throughput and response time, although not by as much as one might expect.

The plot thickens...

@kgriffs

**Thanks** to June Rich for reading drafts of this.

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> Admittedly, the test environment I used was not perfectly controlled due to my use of virtual machines on a shared network. This was a trade-off I was willing to make in order to test application performance in a production cloud hosting environment, which is how many web apps are deployed these days. 
  </li>  
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup> The <a href="http://www.xenoclast.org/autobench/">Autobench website</a> has a good description of these and other options, and how they translate to Httperf parameters.
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup> HTTP/1.0 did not document any support for persistent connections, although some servers support it via the Keep-Alive header.
  </li>
  <li>
    <sup><a name="id-4.ftn" href="#id-4">4</a></sup> Although not tested, I suspect the relative performance between the different implementations would be similar when executing both GET and POST requests, assuming the database is able to keep up with the load. In mixed workloads, the database's write performance is more likely than the application to be a factor in any difference in performance between GET and POST, and my intent in this exercise was to test the app layer, not the DB.
  </li>
</ul>

<script type="text/javascript" src="/assets/js/python-vs-node-vs-pypy-benchmarks.js" />

