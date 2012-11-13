---
layout: post.html
title: Stand back... I'm going to try science!
summary: Check out these results from a round of rigorous performance testing comparing Python, PyPy and Node.js 
tags: [Science Projects]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

The majority of benchmarks posted on the web are derived from testing simple "hello world" apps. Although certainly better than nothing, these tests do not tell us much about real-world performance. The alternative is a more instructive, rigorous approach that requires comparing various implementations of a non-trivial application. Unfortunately, this takes a lot of time that is often hard to justify in the face of dogged competition and looming deadlines. Occasionally, however, the stars *do* align, and one has the chance to conduct such an experiment.

Lately, I've been researching the various merits of Python vs. JavaScript (ala Node.js), in terms of developing web-scale cloud services. In the course of my work, I ported an internal HTTP-based event queuing service from Python (currently running in production) to JavaScript. In a [previous post][last-post], I shared the results from some informal performance testing I did on the two implementations.  

In this post, I'd like to share my results from a second round of more rigorous performance testing, during which the test environment and variables were tightly controlled<sup><a name="id-1" href="#id-1.ftn">1</a></sup>. I switched from [ApacheBench][ab] to [Autobench][autobench]/[Httperf][httperf], in order to generate a more consistent, realistic load. I then used [weighttp][weighttp] to validate my results. 

[last-post]: /2012/10/23/python-vs-node-vs-pypy.html
[autobench]: http://www.xenoclast.org/autobench/
[httperf]: http://www.hpl.hp.com/research/linux/httperf/
[ab]: https://en.wikipedia.org/wiki/ApacheBench
[weighttp]: http://redmine.lighttpd.net/projects/weighttp/wiki

## Environment ##

*Servers*

* [Rackspace Cloud](http://www.rackspace.com/cloud/public/servers/techdetails/) Virtual Machines
  * 4GB RAM (8GB for the weighttp host)
  * 2 vCPUs (4 vCPUs for the weighttp host)
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

* 200 Mbps, per server (300 Mbps for the weighttp host)
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
* Weighttp 0.3 ([with JSON support][weighttp-json])
* Libev 4.11

[httperf-recompiled]: http://gom-jabbar.org/articles/2009/02/04/httperf-and-file-descriptors
[weighttp-json]: https://github.com/lpereira/weighttp

## Actors ##

*Cloud Servers*

* 3 Autobench hosts
* 1 Weighttp host
* 1 API server
* 1 DB server 

*Implementations*

* **Node.js**: V8 + Node.js + Connect
* **Gevent**: CPython + gevent.wsgi + gevent.monkey.patch_all()
* **WsgiRef**: CPython + WSGI Reference Implementation
* **WsgiRef-PyPy**: PyPy + WSGI Reference Implementation

## Benchmarks ##

As in my previous experiment, I benchmarked retrieving a fixed set of events from a message queuing service backed by MongoDB, with alternative service implementations in Python and JavaScript. Unfortunately, I was not able to directly compare PyPy to both CPython *and* Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the message bus prototype using something that works with PyPy, such as Tornado.

For each test, I ran Autobench directly against a single message bus implementation. I set *min\_rate* and *max\_rate*<sup><a name="id-2" href="#id-2.ftn">2</a></sup> to 20 and 2000, respectively, in order to test a wide range of requests per second. This range of "demanded" reqs/sec is represented by the x axis on the graphs below.

I carried out all benchmarks against a single instance of each implementation; no clustering or load-balancing solutions were used (i.e., HAProxy, Gunicorn, Node's *Cluster* module, etc.). 

For those implementations that supported HTTP 1.1<sup><a name="id-3" href="#id-3.ftn">3</a></sup>, I ran each test twice, once with 1 GET<sup><a name="id-4" href="#id-4.ftn">4</a></sup> per connection, and once again with 10 GETs per connection. I denoted this in the results by appending the number of requests per connection to each implementation name, as in *Gevent (1)* and *Gevent (10)*. The results of the latter test may be especially instructive to website developers, since browsers typically perform several requests per connection.

Each request to the message bus returned ~1K of events, encoded as JSON. I also tested *Gevent (10)* and *Node.js (10)* against a larger result set of ~64K events, and against an empty result set (where the server responded to every request with *204 No Content*). Except where noted, only the results from testing the 1K data set appear in the graphs below.

Here are the results. I'll save my (brief) commentary until the end so that you might draw your own conclusions from the data<sup><a name="id-5" href="#id-5.ftn">5</a></sup>.

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

## 64K Smackdown ##

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

For example, the maximum throughput reported by Autobench for *Gevent (1)* was 322.8 req/sec, and occurred at a demand rate<sup><a name="id-2" href="#id-2.ftn">2</a></sup> of 340 req/sec. The closest mapping to httperf's *rate* option for weighttp is *-c* (number of concurrent clients). So, to verify the Autobench/Httperf result for *Gevent (1)*, I ran the following:

    weighttp -n 3000 -t 3 -c 340 -j <URL>

Admittedly, using *-c* in this way was a bit of a fudge, but it worked out OK since many of those 340 req/sec executed concurrently due to network and server latency.

I compared my Autobench and weighttp results by examining the difference in ratios between succeeding implementations, in ascending order of maximum req/sec. In code:

```javascript
{
  s1: Math.abs((max_rps.autobench.wsgiref_pypy / max_rps.autobench.wsgiref) - (max_rps.weighttp.wsgiref_pypy / max_rps.weighttp.wsgiref)),
  s2: Math.abs((max_rps.autobench.wsgiref / max_rps.autobench.gevent) - (max_rps.weighttp.wsgiref / max_rps.weighttp.gevent)),
  s3: Math.abs((max_rps.autobench.gevent / max_rps.autobench.nodejs) - (max_rps.weighttp.gevent / max_rps.weighttp.nodejs))
}
```

Here's a graph showing the difference in relative req/sec reported by the two different tools, where s1, s2, and s3 refer to *Wsgiref-PyPy (1)*:*Wsgiref (1)*, *Wsgiref (1)*:*Gevent (1)*, and *Gevent (1)*:*Node.js (1)*, respectively.

<div id="graph-6" class="flot"></div>

As you can see, the relative performance between implementations varied between 14% and 19%, which is reasonable, given the major differences in implementation between the two tools.

Finally, ordering implementations by peak req/sec, as reported by both tools<sup><a name="id-5" href="#id-5.ftn">5</a></sup>, yields the same sequence in each case, listed below in descending order:

1. Node.js
1. Gevent
1. WsgiRef-PyPy
1. WsgiRef

## Q.E.D. ##

Node.js outperforms Gevent significantly in terms of latency and error rates for small data transfers (~1K). However, for large responses (~64K), the difference between the two platforms is more subtle. Overall, the best-case scenario for Node.js appears to be serving large numbers of concurrent requests for small chunks of data, over a persistent connection.

PyPy performs only slightly better than CPython when using Python's WSGI reference implementation. More work is needed to determine whether PyPy would perform similarly to Node.js given a compatible, non-blocking Python web framework *and* non-blocking MongoDB driver.

Finally, regarding blocking vs. non-blocking I/O frameworks, Gevent outperforms WsgiRef in terms of throughput and response time, although not by as much as one might expect.

The plot thickens...

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> The test environment was not perfectly controlled due to my use of virtual machines on a shared network. On the other hand, my tests do have the benefit of demonstrating web app performance when hosting in the cloud.
  </li>  
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup> The <a href="http://www.xenoclast.org/autobench/">Autobench website</a> has a good description of these and other options, and how they translate to Httperf parameters.
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup> HTTP/1.0 did not document any support for persistent connections, although some servers supported it via the Keep-Alive header.
  </li>
  <li>
    <sup><a name="id-4.ftn" href="#id-4">4</a></sup> I did not test POSTs; I suspect the relative performance between the different implementations would have been similar, although there may have been some minor differences due to the different code paths triggered in servicing writes vs. reads.
  </li>
  <li>
    <sup><a name="id-5.ftn" href="#id-5">5</a></sup> To view the raw data in all its numeric glory, check out the <a type="text/javascript" download="" href="/assets/js/python-vs-node-vs-pypy-benchmarks.js">JavaScript file</a> accompanying this post</a>.
  </li>
</ul>

<script type="text/javascript" src="/assets/js/python-vs-node-vs-pypy-benchmarks.js" />

