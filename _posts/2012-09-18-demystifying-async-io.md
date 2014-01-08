---
layout: post.html
title: How Async I/O Works - And Sometimes Doesn't
summary: Async I/O can be your best friend, or your worst enemy. The devil's in the details.
tags: [Essays]
---

Five Guys sells awesome burgers and fries. I love their food. Each patty is hand-formed, grilled to order, and piled high with crazy toppings like A1, bacon, and green peppers. Ordering at Five Guys goes something like this:

<img src="/assets/images/hacking-table.png" alt="Hacking @ Five Guys" />

1. You tell Nice Person at the counter what you want to eat.
1. Nice Person hands you a receipt with a number on it.
1. You take a seat and do something productive, like hack on some code.
1. Nice Person takes more orders, sending them to Cook.
1. Cook adds patties to the grill as the orders come in, keeping himself busy.
1. Nice Person calls your number when your order is ready.
1. You pick up your order, return to your seat, and get down to business.

Async I/O works in a similar way:

1. Thread tells Kernel what I/O work it wants done (i.e., "please read from this socket" or "please write to this file").
1. Kernel provides a handle to the thread for monitoring the request.
1. Kernel adds the request to a list of items to babysit.
1. Thread continues on with life, periodically checking<sup><a name="id-1" href="#id-1.ftn">1</a></sup> the I/O handle for events.
1. Kernel posts an event to the I/O handle whenever something interesting happens.
1. Thread grabs each event, processing it and checking for more events until the requested operation is complete.

Here's an illustration to help visualize what's happening:

<img class="center" src="/assets/images/async-io.png" alt="Async I/O - Illustration" />

Here we have a (very simplified) execution thread and a fancy box representing the operating system. The thread issues I/O request (1), but since the request is asynchronous, the thread continues working while it waits for the results from (1). In the meantime, the thread issues a second I/O request (2). Eventually, (2) completes, followed closely by (1), generating two I/O events from the kernel. The thread acts on these event, reading the results from first (2), then (1).

# Blocking I/O #

When a thread uses blocking I/O calls, the process looks something like this:

1. Thread tells Kernel what I/O work is needed.
1. Kernel adds the request to a list of items to babysit.
1. Kernel pauses Thread.
1. Kernel wakes up Thread when the I/O request is complete.
1. Thread grabs the results.

Now, contrast the blocking I/O illustration below with the one for async I/O:

<img class="center" src="/assets/images/blocking-io.png" alt="Blocking I/O - Illustration" />

The thread sits idle after issuing I/O request (1). When (1) completes, the thread is allowed to continue its work and issue request (2). Again, this pauses the thread, and the operating system only allows the thread to continue when (2) is complete.

Although blocking I/O is super-simple to use and understand (hooray!), it prevents the thread from doing anything useful whenever an I/O request is pending (booh!). This is **really bad**; compared to reading and writing RAM, I/O on devices such as HDDs and NICs is excruciatingly slow. Blocking on I/O forces threads into hibernation for [millions of CPU-years][io-speed-relative] on every request.

One way of solving the problem is to spawn several worker threads<sup><a name="id-2" href="#id-2.ftn">2</a></sup>. For example, you might create two threads, which I'll cleverly name *Thread A* and *Thread B*. These threads listen for incoming HTTP requests. When Client A connects to Thread A, Thread A blocks while it waits for the kernel to read data from the NIC. Meanwhile, Thread B accepts a connection from Client B and starts servicing it. Now that both threads are busy, what happens when a third client wants to talk? Tragically, the kernel is forced to hold the third request in a queue until one of the threads is free. If too many requests pile up, they will time out before they reach the other end of the queue. Worse, if requests continue to arrive faster than they can be processed, the kernel's queue will eventually fill up, causing the system to block all new connections to the box.

This would be like Five Guys forcing me to stand in line while every single order, for every single person in front of me, is cooked and bagged. Sure, I can check Facebook on my iPhone while I wait, but that hardly counts as being productive. Eventually, I may get so frustrated at waiting that I give up and walk out. This is not good for business (unless you happen to manage the restaurant next door).

<img src="/assets/images/rose.png" alt="Rose" />

In situations like these, asynchronous I/O is exactly what you need. In the above scenario, async functions allow each thread to continue accepting requests, while waiting for bits to travel over the wire. In this way, requests are multiplexed across individual threads of execution, so they spend a lot less time sitting idle, and a lot more time warming the CPU. More clients are served more quickly, with lower latency.

But all is not roses and puppy dogs, my friend.

# I/O Bound vs. CPU Bound #

If your app spends most<sup><a name="id-3" href="#id-3.ftn">3</a></sup> of its time waiting on disk or network I/O, an asynchronous design will usually improve CPU utilization and reduce latency vs. a synchronous model. I say *usually*, because async I/O doesn't help much when your app is only processing a few concurrent tasks. Indeed, some async frameworks come with a significant performance tax that can actually cause higher per-request latency vs. more traditional, synchronous frameworks. This tax only makes sense when you are trying to [scale up][scale] to thousands of simultaneous, [I/O bound][io-bound] tasks. Under heavy load,  multiplexing requests across a small number<sup><a name="id-4" href="#id-4.ftn">4</a></sup> of processes drastically increases the maximum number of concurrent requests a box can handle. Each process can jump back and forth between servicing different requests while waiting for I/O operations to complete in the background.

Some apps, on the other hand, spend most of their time running algorithms and crunching numbers (e.g., audio processing, data categorization, scientific computing, etc.). When a task is [CPU bound][cpu-bound], async I/O certainly won't buy you anything, and is likely to make things worse. If a thread is spending most of its time crunching data, you might as well use blocking-IO and avoid paying any per-request performance tax<sup><a name="id-5" href="#id-5.ftn">5</a></sup>.

# Trade-offs #

Hardware limits us on what we can achieve using blocking I/O in a single thread of execution, so we have to invent ways of simulating concurrent execution. No approach is perfect; it's important to realize this, and research the trade-offs involved in each approach, so that we can make better design decisions.

In other words, use the best tool for the job. :D

@kgriffs

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup> Some operating systems use a push model instead, i.e., the kernel interrupts the
    thread when data is ready or more data is required.
  </li>
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup> Multiprocessing is a common alternative to multi-threading on POSIX systems.
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup> All applications require CPU time, which is why it can be helpful to run multiple threads (or processes) if you've got the cores.
  </li>
  <li>
    <sup><a name="id-4.ftn" href="#id-4">4</a></sup> Running only one thread or process per CPU minimizes expensive context-switching.
  </li>
  <li>
    <sup><a name="id-5.ftn" href="#id-5">5</a></sup> For this reason, servers that need to perform non-trivial processing on a request should hand off that processing to a worker pool.
  </li>

</ul>

[io-bound]: https://en.wikipedia.org/wiki/I/O_bound "I/O Bound - Definition"
[cpu-bound]: https://en.wikipedia.org/wiki/CPU_bound "CPU Bound - Definition"
[io-speed-relative]: http://i.imgur.com/X1Hi1.gif "I/O Latency - Visualized"
[scale]: /2012/09/06/painless-scaling-in-the-cloud.html "Painless Scaling in the Cloud"
