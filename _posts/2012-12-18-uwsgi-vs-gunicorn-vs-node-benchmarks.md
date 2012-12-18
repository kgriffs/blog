---
layout: post.html
title: "uWSGI vs. Gunicorn, or How to Make Python Go Faster than Node"
summary: In which I pit uWSGI against Gunicorn and stumble upon a Python stack that leaves Node.js begging for mercy.
tags: [Science Projects]
id: E3F16CBC-4547-11E2-8358-68BBD1B0F3CE
---

It seems I've finally arrived at the end of my quest to discover a fast, reliable Python stack for serving web APIs that can compete favorably with Node. The funny thing is, I didn't even know it was my quest until I started looking at the surprising results from this latest round of performance testing, in which I pitted uWSGI against Gunicorn. 

When it comes to deploying web APIs, my preference is to use something lean-n-mean for managing local sockets and WSGI workers, leaving macro load balancing, SSL termination, rate limiting and general HTTP heavy-lifting to the big guns (e.g., Stingray, Ngnix, HAProxy, Stud).  

Gunicorn has been my go-to WSGI server for hosting web APIs in production, due to its simplicity, performance, and manageability. Recently I re-discovered uWSGI and was pleasantly suprised to find how far it has come in the past couple of years. I was particularly impressed by uWSGI's high configurability, including lots of production-friendly options. 

Considering that uWSGI and Gunicorn are both pre-forking<sup><a name="id-1" href="#id-1.ftn">1</a></sup> WSGI servers, and given other design similarities, I couldn't help but wonder how each would perform in the ring.  

## Teh Contenders ##

**[uWSGI (1.4.2).][uwsgi]** Here we have what appears to be a devops dream-come-true. Lots of production-friendly configuration options and a pluggable architecture for customizing stats reporting and anything else you can dream up (LZ4 compression, anyone?). uWSGI has matured quite a bit over the past couple of years, and now supports a plethora of languages and deployment options. Nginx supports the uwsgi protocol natively.

**[Gunicorn (0.16.1).][gunicorn]** My go-to WSGI server. Like uWSGI, Gunicorn supports different worker types. IMHO, Gunicorn provides a good balance between performance and usability. It's been performing like a champ for me in production for the better part of a year.

**[Gevent (1.0rc1).][gevent]** This little green machine is mostly about coroutine-based async networking, but includes a pretty decent WSGI server, providing a good baseline that helps put uWSGI and Gunicorn's performance into perspective.

**[Node.js (0.8.14).][nodejs]** I rewrote my event queuing service in JavaScript ala Node to further put uWSGI and Gunicorn's performance into perspective, and to find out how well a Python-based app could compete with one running on the highly-optimized, V8-backed Node platform.

[uwsgi]: http://uwsgi-docs.readthedocs.org/en/latest
[gunicorn]: http://gunicorn.org
[gevent]: http://gevent.org/
[nodejs]: http://nodejs.org/

## Setup ##

The performance testing setup this time around was identical to the one I used previously to [benchmark Gevent, Tornado, Cython, and PyPy][setup]. I brought forward the Cythonized version of my Rawr web framework for this latest round of tests. The Gevent and Node.js numbers you'll see in the charts below were simply carried forward from my previous posts.

All tests involved a single worker and were either self-hosted (in the case of Gevent and Node.js), or used an external WSGI server (in the case of uWSGI and Gunicorn). Workers were configured to use gevent, so they would play nice with my app, which relies on greenlets ala `gevent.monkey.patch_all()`. 

As before, I tested a series of requests to a single event channel which was primed with ~1K of JSON-encoded data (i.e., the httperf workers had to read a little more than 1K per transaction). Keep-alive was not used, modeling the worst-case scenario in which every transaction involved negotiating a new TCP/IP connection.

I used the following command to run uWSGI:

```bash
uwsgi --http :8890 --file rse.py --gevent 2000 -l 1000 -p 1 -L
```

Here's the command I used to run Gunicorn:

```bash
gunicorn \
  -b :8091 -w 1 -k gevent --worker-connections=2000 \
  --backlog=1000 -p gunicorn.pid --log-level=critical rse:app
```

Note that I disabled request logging in both cases.

[setup]: /2012/12/12/gevent-vs-tornado-benchmarks.html

## Results ##

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-1-stdev" class="flot"></div>

## Q.E.D. ##

uWSGI looks like the Python app server to beat, although it's performance did become a bit erratic under high load. Not only is it ridiculously fast, but judging by the docs, uWSGI's gives you a lot of great options for production tuning. 

But what's more, with an optimized web framework and uWSGI on your side, it looks like Python apps can hold their own against Node. 

Now that's something to think about.

@kgriffs

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> The term <em>pre-forking</em>, as used here, simply means that sockets are created before forking child processes, and that those sockets are inherited by the child processes so that they can directly bind to them, saving an extra hop.
  </li>  
</ul>

<script type="text/javascript" src="/assets/js/uwsgi-vs-gunicorn.js" />

