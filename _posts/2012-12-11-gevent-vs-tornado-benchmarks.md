---
layout: post.html
title: Fast Python Web APIs
summary: todo 
tags: [Science Projects]
id: D070292E-25AA-1202-9238-0130128E45A1
---

In this latest round of performance testing, I take Tornado for a *spin* (sorry, couldn't help myself), and also play around with Cython.

Unlike Gevent, Tornado is supported on PyPy, letting me compare PyPy vs. CPython in terms of nonblocking sockets. While I was at it, I also experimented with Cython to see if just compiling a few key modules would give a comparable performance boost to running the entire app under PyPy.

The setup for these tests was identical to the one used in my last post exploring [Python web api performance][prev-post], with the exception that I also added the following to ```/etc/sysctl.conf```.

    # Let the networking stack reuse TIME_WAIT connections
    # when it thinks it's safe to do so
    net.ipv4.tcp_tw_reuse = 1

[prev-post]: /2012/11/13/python-vs-node-vs-pypy-benchmarks.html 

I ported my message bus service to Tornado 2.4.1, with logging disabled via a noop function, and left Tornado's debugging option turned off (the default). In order to make a fair comparison between the Tornado and Gevent implementations, I used [Motor][motor] @ ab024028f2 instead of pymongo in the Tornado code base. 

Motor is a non-blocking fork of pymongo, designed to play nice with Tornado. In the Gevent implementation, I simply used ```gevent.monkey.patch_all()``` to make pymongo non-blocking.

[motor]: http://emptysquare.net/motor/

Let's see how things turned out...

## Gevent vs. Tornado ##

In this test I compared the performance of a Gevent-based implementation of my event bus service to a Tornado-based one that used straight callbacks (the implementation did not use tornado.gen). I used a non-blocking DB driver in both implementations, and both apps were self-hosted (i.e., no external WSGI servers were harmed in the course of this experiment).

Since Tornado comes with its own micro web framework, I used that instead of my custom Rawr framework. 

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-1-stdev" class="flot"></div>

## Gevent: Cython vs. CPython ##

Cython 0.17.2

CyRawr
CyRawr, CyHandler

Compiled the main request controller using Cython.

Throughput (req/sec)
<div id="graph-4-rps" class="flot"></div>

Response Time (ms)
<div id="graph-4-rt" class="flot"></div>

Errors
<div id="graph-4-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-4-stdev" class="flot"></div>

## Tornado: Cython vs. CPython ##

Compiled the main request controller using Cython.

Cython 0.17.2

Throughput (req/sec)
<div id="graph-2-rps" class="flot"></div>

Response Time (ms)
<div id="graph-2-rt" class="flot"></div>

Errors
<div id="graph-2-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-2-stdev" class="flot"></div>

## Tornado: PyPy vs. CPython ##

PyPy 2.0beta1-1

tornado under PyPy crashed with buffer overlow error while attempting 660 tps (also crashed with 1.9, similar performance FYI). - could not get to go beyond after several attempts, as high as it got. Judging by the stack trace, looked like a C Types issue related to tornado.stack_context._StackContextWrapper (is this in the async attribute?)

Throughput (req/sec)
<div id="graph-3-rps" class="flot"></div>

Response Time (ms)
<div id="graph-3-rt" class="flot"></div>

Errors
<div id="graph-3-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-3-stdev" class="flot"></div>

## The Fastest Python Stack ##
Starting to get a good picture of the most performance stack for building web APIs...

Gevent, optimized, micro web framework (to be open-sourced), Cythonize hot code paths.

<script type="text/javascript" src="/assets/js/gevent-vs-tornado.js" />

