---
layout: post.html
title: Python vs. Node vs. PyPy in the Cloud
summary: After playing around with recent versions of PyPy and Node.js, I've discovered some things that may surprise you.
tags: [Research]
id: A60C497E-FD13-11E1-B940-7C49F4FE7012
---

OpenStack has proven that you can build robust, scalable cloud services with Python. On the other hand, startups like Voxer are doing brilliant things with Node.js. That made me curious, so I took some time to learn Node, then ported a web-scale message bus project of mine from Python to JavaScript. 

With Python and Node implementations in hand, I compared the two in terms of performance, community, developer productivity, etc. I also took the opportunity to test-drive PyPy; it seemed appropriate, given that both PyPy and V8<sup><a name="id-1" href="#id-1.ftn">1</a></sup> rely on JIT compilation to boost performance. 

In this particular post, I'd like to share my discoveries concerning Python vs. Node performance. 

## Testing Methodology ##

For each test, I executed 5,000 GETs with ApacheBench (ab). I ran each benchmark 3 times from localhost<sup><a name="id-2" href="#id-2.ftn">2</a></sup> on a 4-core Rackspace Cloud Server<sup><a name="id-3" href="#id-3.ftn">3</a></sup>, retaining only the numbers for the most performant iteration<sup><a name="id-4" href="#id-4.ftn">4</a></sup>.

All stacks were configured to spawn 4 worker processes, backed by a single, local mongod<sup><a name="id-5" href="#id-5.ftn">5</a></sup> for storage. The DB was primed so that each GET resulted in a non-empty response body of about 420 bytes<sup><a name="id-6" href="#id-6.ftn">6</a></sup>.

*~ Insert obligatory benchmark disclaimer here. ~*

## Teh Contenders ##

**CPython (Sync Worker)** 
Python v2.7 + Gunicorn<sup><a name="id-7" href="#id-7.ftn">7</a></sup> v0.14.6 + Rawr<sup><a name="id-8" href="#id-8.ftn">8</a></sup> 

**CPython (Eventlet Worker)** 
Python v2.7 + Gunicorn v0.14.6 + Eventlet v0.9.17 + Rawr

**PyPy (Sync worker)** 
PyPy 1.8 + Gunicorn v0.14.6 + Rawr

**PyPy (Tornado Worker)** 
Gunicorn v0.14.6 + Tornado<sup><a name="id-9" href="#id-9.ftn">9</a></sup>  (footnote - eventlet not supported by PyPy) + Rawr (footnote)

**Node v0.8.11** 
Node v0.8.11 + Cluster + Connect v2.6.0<sup><a name="id-10" href="#id-10.ftn">10</a></sup> (footnote - why chose)

## Throughput Benchmarks ##

In terms of throughput, Node.js is hard to beat. It's almost twice as fast as CPython/Eventlet workers. Interestingly, Node.js spanks Eventlet even while serving a single request at a time. It's obvious that Node's async framework is far more efficient than Eventlet's.

PyPy comes to the rescue, demonstrating the power of a good JIT compiler. The big surprise here is how well the PyPy/Sync workers perform. But there's more to the story... 

Not shown in the graph (below) are a few informal tests I ran to see what would happen at even higher levels of concurrency. At 5,000 concurrent requests, PyPy/Tornado and Node.js exhibited the best performance at ~4100 req/sec, followed closely by PyPy/Sync at ~3800 req/sec, then CPython/Sync at ~2200 req/sec. I couldn't get CPython/Eventlet to finish all 5,000 requests without socket errors.

<img class="block" src="/assets/images/node-bench/throughput.png" alt="Python vs. PyPy vs. Node.js - Throughput Benchmark" />

## Latency Benchmarks ##

CPython/Eventlet demonstrated a lot of per-request overhead, turning around requests about 30% slower (in the worst case) than non-evented CPython workers. Node, PyPy/Sync, and PyPy/Tornado showed similar latency in my tests.

<img class="block" src="/assets/images/node-bench/latency.png" alt="Python vs. PyPy vs. Node.js - Latency Benchmark" />

## Stability Benchmarks ##

With a high number of concurrent connections, PyPy's performance was most consistent across all 5,000 requests, followed closely by CPython/Sync. Node was more inconsistent than I expected, given its finely-tuned I/O subsystem.

<img class="block" src="/assets/images/node-bench/stability.png" alt="Python vs. PyPy vs. Node.js - Stability Benchmark" />

## Conclusions ##

Node's [asynchronous](/2012/09/18/demystifying-async-io.html) subsystem incurrs far less overhead than Eventlet, and is slightly faster than Tornado running under PyPy. However, it appears that for moderate numbers of concurrent requests, the overhead inherent in any async framework simply isn't worthwhile (footnote - sync only behind evented -slowloris). I.e., async only makes sense in the context of serving several thousand concurrent requests per second.

CPython's lackluster performance makes a strong case for migrating to PyPy for existing projects, and for considering Node.js as a viable alternative to Python for new projects. That being said, PyPy is not nearly as battle-tested as CPython; caveat emptor!

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> Node uses Google's V8 JavaScript engine under the hood. 
  </li>
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup> Running ab on the same box as the server avoids networking anomalies that could bias test results.
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup> CentOs 5.5, 8 GB RAM, ORD region, first-generation cloud server platform.
  </li>
  <li>
    <sup><a name="id-4.ftn" href="#id-4">4</a></sup> What can I say? I'm an insufferable optimist.
  </li>
  <li>
    <sup><a name="id-5.ftn" href="#id-5">5</a></sup> A lot of FUD has gone around re MongoDB. I'm convinced that most bad experiences with Mongo are due to one or more of the following: (1) Developers conciously (or subconciously) expecting MongoDB to act like an RDBMS, (2) the perpetuation of the myth that MongoDB is not durable, and (3) trying to run MongoDB on servers with slow disks and/or insufficient RAM.
  </li>
  <li>
    <sup><a name="id-6.ftn" href="#id-6">6</a></sup> The response body was chosen as an example of a typical JSON document that might be returned from the message bus service.
  </li>
  <li>
    <sup><a name="id-7.ftn" href="#id-7">7</a></sup> Gunicorn is a very fast WSGI worker proxy, similar to Node's Cluster module. Gunicorn supports running various worker types, including basic syncronous workers, Eventlet workers, and Tornado workers.
  </li>
  <li>
    <sup><a name="id-8.ftn" href="#id-8">8</a></sup> Lispem.
  </li>
  <li>
    <sup><a name="id-9.ftn" href="#id-9">9</a></sup> Lispem.
  </li>
  <li>
    <sup><a name="id-10.ftn" href="#id-10">10</a></sup> Lispem.
  </li>
</ul>

based on extensive benchmarking, i ended up writing a custom micro web-services framework. Don't use webob for parsing requests - too slow.

sync only behind evented -slowloris, 
=

