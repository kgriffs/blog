---
layout: post.html
title: Tornado vs. Gevent - Benchmarks
tags: [Science Projects]
id: D070292E-25AA-1202-9238-0130128E45A1
---

In this latest round of performance testing, I take the Tornado web framework for a spin (heh, couldn't help myself), and also play around with Cython. 

<img class="right" src="/assets/images/python-tornado.png" width="300px" height="300px" alt="Poor Cloud Ideas (Thrown Away)" />

After FriendFeed was acquired several years ago, [Tornado][tornado] stagnated a bit, but this past year the community has been hard at work. Version 2.0 came out this past June, and the framework is now at 2.4.1 (at the time of this writing).

Unlike Gevent, Tornado works on [PyPy][pypy], making it possible to compare PyPy vs. CPython in terms of nonblocking sockets. While I was at it (famous last words), I also experimented with [Cython][cython] to see if just compiling a few key modules would give a comparable performance boost to running the entire app under PyPy.

My setup for these tests was identical to the one used in my last post exploring [Python web api performance][prev-post], with the exception that I also added the following to ```/etc/sysctl.conf```.

    # Let the networking stack reuse TIME_WAIT connections
    # when it thinks it's safe to do so
    net.ipv4.tcp_tw_reuse = 1

[tornado]: http://www.tornadoweb.org
[pypy]: http://pypy.org/
[cython]: http://cython.org/
[prev-post]: /2012/11/13/python-vs-node-vs-pypy-benchmarks.html 

I ported my message bus service to Tornado 2.4.1, with logging disabled via a noop function, and left Tornado's debugging option turned off (the default). In order to make a fair comparison between the Tornado and Gevent implementations, I used Motor (@ab024028f2) instead of pymongo in the Tornado code base so that the DB drivers were non-blocking in both implementations.

[Motor][motor] is a non-blocking fork of pymongo, designed to play nice with Tornado. In the Gevent implementation, I simply used ```gevent.monkey.patch_all()``` to make pymongo non-blocking.

For all tests, only one request was performed per connection (no keep-alive or pipelining this time around). 

---

*<strong>Protip:</strong> You can view and play with the raw result data by downloading the <a type="text/javascript" download="" href="/assets/js/gevent-vs-tornado.js">Flot data file</a> that I used to draw the graphs below.*

---

[motor]: http://emptysquare.net/motor/

## Gevent vs. Tornado ##

In this test I compared the performance of a Gevent-based implementation of my event bus service to one based on Tornado, the latter being implemented with the callback async style (no tornado.gen). Since Tornado comes with its own micro web framework, I used that in lieu of my own (Rawr).

As mentioned elsewhere, I used a non-blocking MongoDB driver in both implementations. Also noteworthy is that both implementations were self-hosted using each frameworks' native web server (gevent.wsgi in the case of Gevent). 

**Throughput (req/sec)**
<div id="graph-1-rps" class="flot"></div>

**Response Time (ms)**
<div id="graph-1-rt" class="flot"></div>

**Errors**
<div id="graph-1-errors" class="flot"></div>

**Standard Deviation, Throughput (req/sec)**
<div id="graph-1-stdev" class="flot"></div>

## Cython vs. CPython vs. Node.js ##

In this benchmark, I tested the performance of Cython 0.17.2 running under CPython 2.7.3, by compiling a few core modules with Cython and comparing the application's performance with those vs. the regular *.pyc ones. 

In the graph keys shown below, CyRawr denotes a run where only my custom web framework, Rawr, was compiled with Cython. CyHandler indicates that the message request handler was also compiled with Cython before executing the application.

I also included my [previous Node.js benchmarks][prev-post] to help put these results in context.

**Throughput (req/sec)**
<div id="graph-4-rps" class="flot"></div>

**Response Time (ms)**
<div id="graph-4-rt" class="flot"></div>

**Errors**
<div id="graph-4-errors" class="flot"></div>

**Standard Deviation, Throughput (req/sec)**
<div id="graph-4-stdev" class="flot"></div>

## Tornado: Cython vs. CPython ##

This benchmark was similar to the one performed above, except it tested Cython-compiled modules running under the Tornado framework and web server.

**Throughput (req/sec)**
<div id="graph-2-rps" class="flot"></div>

**Response Time (ms)**
<div id="graph-2-rt" class="flot"></div>

**Errors**
<div id="graph-2-errors" class="flot"></div>

**Standard Deviation, Throughput (req/sec)**
<div id="graph-2-stdev" class="flot"></div>

## Tornado: PyPy vs. CPython ##

Unlike Gevent, Tornado is mostly compatible with PyPy, so I was able to benchmark Tornado running under CPython 2.7.3 vs. PyPy 2.0beta1-1.

Unfortunately, I wasn't able to test Tornado's performance running under PyPy with request attempts over ~660/sec. Tornado crashed<sup><a name="id-1" href="#id-1.ftn">1</a></sup> with a buffer overflow error several times in a row at this load. I verified that this crash wasn't caused by a PyPy 2.x bug, by running a quick test under 1.9 and observing identical behavior. 

**Throughput (req/sec)**
<div id="graph-3-rps" class="flot"></div>

**Response Time (ms)**
<div id="graph-3-rt" class="flot"></div>

**Errors**
<div id="graph-3-errors" class="flot"></div>

**Standard Deviation, Throughput (req/sec)**
<div id="graph-3-stdev" class="flot"></div>

## Conclusions ##

Gevent is very fast, with a good ecosystem, plus a ridiculously simple async programming model--all thanks to the magic of greenlets, libev and monkey-patching.

Tornado is not as fast as Gevent, and is hampered by the immature Motor library. Perhaps owing to the fact that Tornado was originally written to handle large numbers of *persistent* connections, the framework was never optimized for frequent connection negotiations, making it lag behind Gevent for this use case. Note, however, that Tornado did seem to handle large numbers of connection requests more gracefully than did Gevent, as indicated by the former's consistently low error rate (under CPython).

Surprisingly, PyPy did not significantly speed up my Tornado-based implementation. I suspect the lackluster performance of greenlets (used by Motor) under PyPy, which may have caused the app to bottleneck at the DB library.

All things considered, Gevent + Cython appears to be the best choice of platform for building a Python-based web api, particularly if you're using MongoDB. Gevent provides fast, non-blocking sockets and an elegant synchronous-on-asynchronous programming model that is officially supported by pymongo, while Cython compensates well for Gevent's incompatibility with PyPy. 

In my next post, I'll share results from testing Gevent's web server against uWSGI, Gunicorn, and Node. Stay tuned...

@kgriffs

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> Judging by the stack trace, there was a native module/ctypes issue, related to <em>tornado.stack_context._StackContextWrapper</em>. It may have been related to Motor, but I can't say for sure pending further investigation.
  </li>  
</ul>

<script type="text/javascript" src="/assets/js/gevent-vs-tornado.js" />

