---
layout: post.html
title: uWSGI vs. Gunicorn Benchmarks
summary: todo 
tags: [Science Projects]
id: D0EF76FC-43B8-11E2-B1A9-67ADD1B0F3CE
---

Same setup as last time, and bringing forward Gevent 1K, CyRawr and Node.js as baselines.

Testing two pre-forking WSGI servers with 1 worker each. Pre-forking means the sockets are bound before forking child processes which then share those sockets.

gunicorn 0.16.1
uwsgi 1.4.2

gunicorn -b :8091 -w 1 -k gevent --worker-connections=2000 --backlog=1000 -p gunicorn.pid --log-level=critical rse:app

uwsgi --http :8890 --file rse.py --gevent 2000 -l 1000 -p 1 -L

disabled logging for all intents and purposes.

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

