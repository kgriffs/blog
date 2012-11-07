---
layout: post.html
title: Stand back... I'm going to try science!
summary: Check out these results from a round of rigorous performance testing comparing Python, PyPy and Node.js 
tags: [Science Projects]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

Most framework benchmarks posted on the web are derived from testing simple "hello world" apps. These results do not accurately depict real-world performance of these frameworks. On the other hand, taking a more instructive, rigorous approach requires comparing various implementations of a non-trivial application. This is Not Fun&trade;. Occasionally, however, the stars *do* align, and one has the chance to conduct such an experiment.

Lately, I've been researching the various merits of Python vs. JavaScript (ala Node.js), in terms of developing web-scale cloud services. In the course of my work, I decided to port a highly-optimized, HTTP-based message bus (currently running in production) from Python to JavaScript. In a [previous post][last-post], I shared the results from some informal performance testing I did on the two implementations.  

In this post, I'd like to share my results from a second round of more rigorous performance testing. In this round, the environment and variables under test were much more tightly controlled than before. In addition, I switched from using [ApacheBench][ab] to [Autobench][autobench]/[Httperf][httperf], in order to generate a higher and more consistent load against the server than ab could deliver. I used [weighttp][weighttp] to verify the results. 

[last-post]: /2012/10/23/python-vs-node-vs-pypy.html
[autobench]: http://www.xenoclast.org/autobench/
[httperf]: http://www.hpl.hp.com/research/linux/httperf/
[ab]: https://en.wikipedia.org/wiki/ApacheBench
[weighttp]: http://redmine.lighttpd.net/projects/weighttp/wiki

## Environment ##

Servers

* [Rackspace Cloud Server](http://www.rackspace.com/cloud/public/servers/techdetails/)
  * 4GB RAM (8GB for weighttp host)
  * 2 vCPUs (4 vCPUs for weighttp host)
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
* Httperf 0.9.0 ([recompiled][httperf-recompiled])
* Weighttp 0.3 ([with JSON support][weighttp-json])
* Libev 4.11

[httperf-recompiled]: http://gom-jabbar.org/articles/2009/02/04/httperf-and-file-descriptors
[weighttp-json]: https://github.com/lpereira/weighttp

## Actors ##

Cloud Servers

* 3 Autobench hosts
* 1 Weighttp host
* 1 API server
* 1 DB server 

Implementations

* **Node.js**: V8 + Node.js + Connect
* **Gevent**: CPython + gevent.wsgi + gevent.monkey.patch_all()
* **WsgiRef**: CPython + WSGI Reference Implementation
* **WsgiRef-PyPy**: PyPy + WSGI Reference Implementation

## Benchmarks ##

As in my previous experiment, I benchmarked retrieving a fixed set of events from a message queuing service backed by MongoDB, with alternative service implementations in Python and JavaScript. Unfortunately, I was not able to formally compare PyPy to both CPython *and* Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the message bus prototype using the Tornado or Cyclone frameworks.

For each test, I ran Autobench directly against a single message bus implementation. I set --min\_rate and --max\_rate to 20 and 2000, respectively, in order to test a wide range of requests per second (represented by the x axis of the graphs below). The [Autobench website][autobench] has a good description of these options, and how they translate to [Httperf][httperf] parameters.

I carried out all benchmarks against a single instance of each implementation; no clustering solutions were used (e.g., Gunicorn or Node's *Cluster* module). 

For those implementations that supported HTTP 1.1 pipelining, I ran each test twice, once with 1 GET request per connection, and once again with 10 GET requests per connection. I denoted this in the results by appending the number of requests per connection to each implementation name, as in *Gevent (1)* and *Gevent (10)*. The results of the latter test may be especially instructive to website developers, since browsers typically perform several requests per connection.

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

Throughput (req/sec)
<div id="graph-2-rps" class="flot"></div>

Response Time (ms)
<div id="graph-2-rt" class="flot"></div>

Errors
<div id="graph-2-errors" class="flot"></div>

Standard Deviation (req/sec)
<div id="graph-2-stdev" class="flot"></div>

## Sanity Check ##

To check my Autobench results, I ran a separate test using weighttp, configured with the same rate at which autobench reported the highest requests per second for each message bus implementation (testing at 1 request per connection). 

For example, the maximum throughput reported by Autobench for *Gevent (1)* was 322.8 req/sec, and occurred at a demand rate[fn-see-also--rate](http://www.hpl.hp.com/research/linux/httperf/httperf-man-0.9.txt) of 340 req/sec. The closest mapping to httperf's --rate option for weighttp is -c (number of concurrent clients). So, to verify the Autobench/httperf result for *Gevent (1)*, I ran the following:

    weighttp -n 3000 -t 3 -c 340 -j <URL>

Admittedly, using -c in this way is a bit of a fudge, but it works out OK since most of those 340 req/sec happen concurrently due to network and server latency.

I compared my Autobench and weighttp results by examining the difference in ratios between succeeding implementations, in ascending order of maximum req/sec. In code:

```javascript
    {
      s1: Math.abs((max_rps.autobench.wsgiref_pypy / max_rps.autobench.wsgiref) - (max_rps.weighttp.wsgiref_pypy / max_rps.weighttp.wsgiref)),
      s2: Math.abs((max_rps.autobench.wsgiref / max_rps.autobench.gevent) - (max_rps.weighttp.wsgiref / max_rps.weighttp.gevent)),
      s3: Math.abs((max_rps.autobench.gevent / max_rps.autobench.nodejs) - (max_rps.weighttp.gevent / max_rps.weighttp.nodejs))
    }
```

As shown below, the differences were fairly minor, lending credibility to the Autobench results.

<div id="graph-6" class="flot-short"></div>

## Q.E.D. ##

Node.js outperforms Gevent significantly in terms of latency and error rates for small data transfers (~1K). However, for large responses (~64K), the difference between the two platforms is not nearly as stark. Overall, the best-case scenario for Node.js appears to be serving large numbers of concurrent, pipelined requests for small chunks of data.

PyPy performs only slightly better than CPython when using Python's WSGI reference implementation. More work is needed to determine whether PyPy would perform similarly to Node.js given a compatible, non-blocking Python web framework.

Finally, regarding blocking vs. non-blocking I/O frameworks, Gevent demonstrated a clear advantage over WsgiRef in terms of throughput and response time. However, Gevent goes to heck when super-saturated judging by the error rates demonstrated by my tests.

<script type="text/javascript" src="/assets/js/python-vs-node-rematch.js" />

