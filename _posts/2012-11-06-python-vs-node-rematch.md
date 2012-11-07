---
layout: post.html
title: Everybody stand back... <br/>I'm going to try science!
summary: Check out these results from a round of rigourous performance testing between Python and Node.js 
tags: [Science Projects]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

Most framework benchmarks posted on the web are derived from testing simple "hello world" apps. These results do not accurately depict real-world performance of these frameworks. On the other hand, taking a more instructive, rigourous approach requires comparing various implementations of a non-trivial application. This is Not Fun&trade;. Occasionally, however, the stars *do* align, and one has the chance to conduct such an experiment.

Lately, I've been researching the various merits of Python vs. JavaScript (ala Node.js), in terms of developing web-scale cloud services. In the course of my work, I decided to port a highly-optimized, HTTP-based message bus (currently running in production) from Python to JavaScript. In a [previous post][last-post], I shared the results from some informal performance testing I did on the two implementations.  

In this post, I'd like to share my results from a second round of more rigourous performance testing. In this round, the environment and variables under test were much more tightly controlled than before. In addition, I switched from using [ApacheBench][ab] to [Autobench][autobench]/[Httperf][httperf], in order to generate a higher and more consistent load against the server. 

As in my previous experiment, I benchmarked retrieving a fixed set of events from a message queueing service backed by MongoDB, with alternative service implementions in Python and JavaScript. Unfortunately, I was not able to formally compare PyPy to both CPython *and* Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the message bus prototype in Tornado or Cyclone [fn-not-fair-to-compare-against-gevent-with-monkeypatched-too-different].

[last-post]: /2012/10/23/python-vs-node-vs-pypy.html
[autobench]: http://www.xenoclast.org/autobench/
[httperf]: http://www.hpl.hp.com/research/linux/httperf/
[ab]: https://en.wikipedia.org/wiki/ApacheBench

## Environment ##

Servers

* [Rackspace Cloud Server](http://www.rackspace.com/cloud/public/servers/techdetails/)
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

Network

* 200 Mbps, per server
* Internal network interface (10.x.x.x)

Python

* CPython 2.7.3
* PyPy 1.9.0 
* Gevent 1.0rc1
* PyMongo 2.3
* WebOb 1.2.3

Node.js

* Node.js 0.8.14
* Connect 2.5.0
* node-mongodb-native 1.1.11

Other

* MongoDB 2.2
* Autobench 2.1.2
* Httperf 0.9.0, compiled from source after editing /usr/include/bits/typesizes.h to [increase the hard-coded limit on file descriptors](http://gom-jabbar.org/articles/2009/02/04/httperf-and-file-descriptors). 

## Setup ##

* 3 Autobench hosts
* 1 API server
* 1 DB server 

The implementations:

* Node.js + Connect (Node.js)
* CPython + Gevent (Gevent)
* CPython + WSGI Reference Implementation (WsgiRef)
* PyPy + WSGI Reference Implementation (WsgiRef-PyPy)

For each test, I ran [Autobench](http://www.xenoclast.org/autobench/) directly against a single message bus implementation, testing a range of requests per second, from 20 to 2000, inclusive (represented by the x axis on the graphs). I carried out all benchmarks against a single instance of each implementation; no clustering solutions were used (e.g., Gunicorn or Node's *Cluster* module). 

For those implementations that supported HTTP 1.1 Keep-Alive, I ran each test twice, once with 1 GET request per connection, and once again with 10 GET requests per connection. I denoted this in the results by appending the number of requests per connection to each implementation name, as in *Gevent (1)* and *Gevent (10)*. The results of the latter test may be especially instructive to website developers, since browsers typically perform several requests per connection.

Each request to the message bus returned ~1K of events, encoded as JSON. I also tested *Gevent (10)* and *Node.js (10)* against a larger result set of ~64K events. Except where noted, only the results from testing the 1K data set are graphed.

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

## 1K JSON vs. 64K JSON ##

<div id="graph-2a" class="flot"></div>
<div id="graph-2b" class="flot"></div>

## Q.E.D. ##

...need to get gevent working with pypy, or write a native pypy framework, including non-blocking sockets, pymongo support (or would it just work?)

<script type="text/javascript" src="/assets/js/python-vs-node-rematch.js" />

