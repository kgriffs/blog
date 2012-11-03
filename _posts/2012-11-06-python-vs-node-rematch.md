---
layout: post.html
title: Python vs. Node - Stand back... I'm going to try science!
summary: Check out these results from a round of more formal, apples-to-apples performance testing between Python and Node.js 
tags: [Science Projects]
id: D074292E-25AA-11E2-9238-0137128E45A1
---

In my last round of performance testing, described in *Python vs. Node vs. PyPy*, my informal methodology created several ambiguities in the test results [fn-still-useful]. To address these ambiguities, I performed another round of tests using a more rigorous approach than before. The benchmarks I performed in this latest round still cover only one problem domain and a specific server environment, so  you would be wise to validate my results against your own performance tests.

Unfortunately, I was not able to formally compare PyPy to CPython and Node.js, since Gevent is currently incompatible with PyPy, and I did not have the luxury of reimplementing the message bus prototype in Tornado or Cyclone [fn-not-fair-to-compare-against-gevent-with-monkeypatched-too-different].

## The Benchmark ##

## The Contenders ##

## The Results ##

<div id="graph-1a" class="flot"></div>
<div id="graph-1b" class="flot"></div>
<div id="graph-1c" class="flot"></div>
<div id="graph-2a" class="flot"></div>
<div id="graph-2b" class="flot"></div>
<div id="graph-3a" class="flot"></div>
<div id="graph-3b" class="flot"></div>
<div id="graph-4a" class="flot"></div>
<div id="graph-4b" class="flot"></div>

## Conclusions ##

...need to get gevent working with pypy, or write a native pypy framework, including non-blocking sockets, pymongo support (or would it just work?)

<script type="text/javascript">
$(function () {
    var d1 = [];
    for (var i = 0; i < 14; i += 0.5)
        d1.push([i, Math.sin(i)]);

    var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];

    // a null signifies separate line segments
    var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];
    
    $.plot($("#graph-1a"), [ d1, d2, d3 ]);
});
</script>

