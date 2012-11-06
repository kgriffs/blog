---
layout: post.html
title: Python vs. Node - Stand back... I'm going to try science!
summary: Check out these results from a round of more formal, apples-to-apples performance testing between Python and Node.js 
tags: [Science Projects]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

&nbsp;

In my last round of performance testing, described in [Python vs. Node vs. PyPy][last-article], my informal methodology created several ambiguities in the test results [fn-still-useful]. To address these ambiguities, I performed another round of tests using a more rigorous approach than before. The benchmarks I performed in this latest round still cover only one problem domain and a specific server environment, so  you would be wise to peform your own performance testing before making any decisions based on my results.

As in my previous experiment, I will benchmark GETing events from a non-trivial cloud message bus[fn-vs-trivial-hello-worl-all-too-common], with alternative implementions in Python and JavaScript. The message bus API is HTTP-based, making it easy to use standard benchmarking tools. 

Unfortunately, I was not able to formally compare PyPy to both CPython *and* Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the message bus prototype in Tornado or Cyclone [fn-not-fair-to-compare-against-gevent-with-monkeypatched-too-different].

[last-article]: /2012/10/23/python-vs-node-vs-pypy.html

## Environment ##

Servers

* [Rackspace Cloud Server](http://www.rackspace.com/cloud/public/servers/techdetails/): 4GB RAM, 2 vCPUs, NextGen, ORD
* Arch Linux 2012.08, x86_64, with a full system upgrade (pacman -Syu)
* Kernel: linux-3.6.5-1
* Set nofile to 10000 in /etc/security/limits.conf
* Tuned several kernel parameters in [/etc/sysctl.conf](https://gist.github.com/4027835) to handle a large number of TCP requests and socket churn

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

I used an [Autobench](http://www.xenoclast.org/autobench/) cluster to create a series of HTTP requests against the API server over Rackspace's internal, server-to-server network. 5 servers were configured per the above environment, specifically:

* 3 Autobench hosts
* 1 API server
* 1 DB server 

For each test, I ran Autobench directly against a single cloud message bus implementation, testing a range of requests per second, from 20 to 2000, inclusive (represented by the x axis shown on the graphs presented below).

The implementations:

* Node.js + Connect (Node.js)
* CPython + Gevent (Gevent)
* CPython + WSGI Reference Implementation (WsgiRef)
* PyPy + WSGI Reference Implementation (WsgiRef-PyPy)

For those implementations that supported HTTP 1.1 Keep-Alive, I ran each test twice, once with 1 request per connection, and once again with 10 requests per connection. I denoted this in the results by appending the number of requests per connection to each implementation name. For example, "Gevent (1)" vs. "Gevent (10)". 

As a final note, I carried out all benchmarks against a single instance of each implementation; no clustering solutions were used (e.g., Gunicorn or Node's *Cluster* module). 

## Gevent vs. Node.js ##

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation (req/sec)
<div id="graph-1-stdev" class="flot"></div>

## 1K vs. 64K ##

<div id="graph-2a" class="flot"></div>
<div id="graph-2b" class="flot"></div>

## PyPy vs. CPython ##

Throughput (req/sec)
<div id="graph-4-rps" class="flot"></div>

Response Time (ms)
<div id="graph-4-rt" class="flot"></div>

Errors
<div id="graph-4-errors" class="flot"></div>

## Sync vs. Async ##

Throughput (req/sec)
<div id="graph-5-rps" class="flot"></div>

Response Time (ms)
<div id="graph-5-rt" class="flot"></div>

Errors
<div id="graph-5-errors" class="flot"></div>

## Q.E.D. ##

<div id="graph-6" class="flot"></div>

...need to get gevent working with pypy, or write a native pypy framework, including non-blocking sockets, pymongo support (or would it just work?)

<script type="text/javascript" src="/assets/js/python-vs-node-rematch.js" />

