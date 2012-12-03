---
layout: post.html
title: Circus and Chaussette Benchmarks
summary: todo 
tags: [Science Projects]
id: 75893C5E-3D6D-11E2-865F-61B5D1B0F3CE
---

Also tested gevent vs meinheld (but still using gevent for monkey-patching).

testing against CyRawr.

meinheld 


```meinheld.set_access_logger(None)```

Same envs as last time, except enabled this flag to avoid using up all available sockets during benchmarking

"Let the networking stack reuse TIME_WAIT connections when it thinks it's safe to do so"
```net.ipv4.tcp_tw_reuse = 1```

1. Gevent self-hosted
1. Meinheld self-hosted
1. Putting on socks (gevent, meinheld)
1. Bring on the clowns

## Results ##

Throughput (req/sec)
<div id="graph-1-rps" class="flot"></div>

Response Time (ms)
<div id="graph-1-rt" class="flot"></div>

Errors
<div id="graph-1-errors" class="flot"></div>

Standard Deviation for Throughput (req/sec)
<div id="graph-1-stdev" class="flot"></div>

<script type="text/javascript" src="/assets/js/gevent-vs-meinheld.js" />

