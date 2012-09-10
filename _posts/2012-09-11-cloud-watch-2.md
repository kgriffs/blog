---
layout: post.html
title: Cloud Watch, Issue &#35;2
summary: Learn about wolf-fence debugging, hacking corporate culture, lessons learned from developing StarCraft, and more.
tags: [News]
id: 0F76E416-FB78-11E1-BDA0-80A0F4FE7011
---

*Cloud Watch is a semi-regular newsletter showcasing recent posts on software and cloud engineering, gathered from around the intertubes.*

# Tools #

**[Wolf-Fence Debugging with Git][bisect]**. Wolf-fence debugging uses divide-and-conquer to eliminate possible locations of bugs in your code. This is a particularly good technique for tracking down sneaky memory bugs and race conditions. Check out git-bisect for a way to use wolf-fence debugging to quickly home in on a commits in sheep's clothing.

**[Retro Visio][ascii]**. Asciiflow is a fun alternative to Visio, perfect for adding an artistic touch to README files, tech talks, and your favorite BBS.

**[Faster Builds with Ninja][ninja]**. Check out this complement to gyp and CMake that performs incremental builds faster than Chuck Norris.

[bisect]: http://git-scm.com/docs/git-bisect
[ascii]: http://www.asciiflow.com
[ninja]: http://martine.github.com/ninja/

# DevOps

**[Hack Your Corporate Culture][hack]**. Getting to web-scale requires a particular kind of tech culture. Jesse Robbins of Amazon and Opscode fame gives some pragmatic tips at Velocity 2012 on how to create a culture of technical excellence.

TL;DW

1. Start small, build trust & safety
1. Create champions
1. Use metrics to build confidence
1. Celebrate successes
1. Exploit compelling events

**[State of TLS][tls]**. httpd hacker Paul Querna shares some data he's collected on the adoption of several TLS extensions. SNI adoption isn't as far along as you might hope. On the other hand, supporting session tickets can be a smart move.

[hack]: http://www.youtube.com/watch?v=OU8ihx3nT6I
[tls]: http://journal.paul.querna.org/articles/2012/09/07/adoption-of-tls-extensions/

# NoSQL # #

**[Secure Your Big Data with Accumulo][accumulo]**. Developed by the NSA then open-sourced about a year ago, Accumulo is unique in that it offers cell-level security, providing a more fine-grained approach to complying with regulations such as HIPPA. Recently, a startup called Sqrrl announced their plans to commercialize Accumulo. From the README:

> Apache Accumulo is a sorted, distributed key/value store based on Google's BigTable design. It is built on top of Apache Hadoop, Zookeeper, and Thrift. It features a few novel improvements on the BigTable design in the form of cell-level access labels and a server-side programming mechanism that can modify key/value pairs at various points in the data management process.

**[MongoDB 2.2 Released][mongo22]**. This new release contains some serious [performance improvements][mongoperf], as well as the long-awaited TTL collections feature.

[accumulo]:http://siliconangle.com/blog/2012/08/20/accumulo-why-the-world-needs-another-nosql-database/
[mongo22]:http://docs.mongodb.org/manual/release-notes/2.2/
[mongoperf]: http://blog.serverdensity.com/goodbye-global-lock-mongodb-2-0-vs-2-2/

# Hackers at Work #

**[What's the author of *Modern C++ Design* doing at Facebook][alexandrescu]**? This post was from this past January, but was cool enough that I wanted to still include it. Read Andrei's thoughts on machine learning and languages such as PHP, C++, and (my old friend) D.

**[Lessons Learned on the Road to StarCraft][sc]**. Patrick Wyatt, long-time game developer, shares anecdotes from his time working on the genre-defining StarCraft game at Blizzard.

**[The Art and Science of Software Engineering][carmack]**. Legendary game engine hacker John Carmack discusses a recent realization of his, that writing software is a lot less about computer science, and a lot more about social engineering.

[sc]: http://www.codeofhonor.com/blog/tough-times-on-the-road-to-starcraft
[carmack]: http://blogs.uw.edu/ajko/2012/08/22/john-carmack-discusses-the-art-and-science-of-software-engineering
[alexandrescu]: http://www.serversidemagazine.com/news/10-questions-with-facebook-research-engineer-andrei-alexandrescu/
