---
layout: post.html
title: uWSGI vs. Gunicorn -Or- How to Make Python Go Faster than Node
summary: In which I pit uWSGI against Gunicorn and stumble upon a Python stack that leaves Node.js begging for mercy.
tags: [Science Projects]
id: E3F16BBC-4547-11E2-8358-68BBD1B0F3CE
---

It seems I've finally arrived at the end of my quest to discover a fast, reliable Python stack for serving web APIs that can compete favorably with Node. The funny thing is, I didn't even know this was my quest until I started looking at the surprising results from this latest round of performance testing, in which I pitted uWSGI against Gunicorn. 

When it comes to deploying web APIs, my preference has been to use something lean-and-mean for managing local sockets and workers, leaving macro load balancing, SSL termination, rate limiting and general HTTP heavy-lifting to the big boys (i.e., Stingray, Ngnix, HAProxy, Stud, etc.).  

Gunicorn has been my go-to WSGI server for hosting web APIs in production, due to its simplicity, performance, and manageability. Recently I re-discovered uWSGI and was pleasantly suprised to discover how far it has come in the past couple of years. I was impressed by the high configurability and production-friendly options of uWSGI, and decided it was time to re-evaluate my WSGI server of choice.

## Setup ##

The performance testing setup this time around was identical to the one I used previously to [benchmark Gevent, Tornado, Cython, and PyPy][setup]. All tests involved a single worker and were either self-hosted (in the case of Gevent and Node.js), or used an external WSGI server (in the case of uWSGI and Gunicorn).

## Teh Contenders ##

**[uWSGI.][uwsgi]** Here we have a devops-dream-come-true. Lots of production-friendly configuration options and a pluggable architecture for customizing stats reporting and anything else you can dream up.

The Gevent and Node.js benchmarks you'll see graphed below were carried forward from my previous posts. 

uWSGI and Gunicorn to host my WSGI app

  I pit uWSGI against Gunicorn and stumble upon a Python stack that leaves Node.js in the dust. 

WSGI python apps can be hosted in many ways; personally, I prefer using a lean-and-mean web server that manages my worker processes for me and is highly configurable with production-friendly options.

Same setup as last time, and bringing forward Gevent 1K, CyRawr and Node.js as baselines.

Testing two pre-forking WSGI servers with 1 worker each. Pre-forking means the sockets are bound before forking child processes which then share those sockets.

gunicorn 0.16.1
uwsgi 1.4.2

gunicorn -b :8091 -w 1 -k gevent --worker-connections=2000 --backlog=1000 -p gunicorn.pid --log-level=critical rse:app

uwsgi --http :8890 --file rse.py --gevent 2000 -l 1000 -p 1 -L

disabled logging for all intents and purposes.

[setup]: /2012/12/12/gevent-vs-tornado-benchmarks.html
[wsgi]: http://uwsgi-docs.readthedocs.org/en/latest/
[gunicorn]: 

## Results ##

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-1-stdev" class="flot"></div>

<script type="text/javascript" src="/assets/js/uwsgi-vs-gunicorn.js" />

