---
layout: post.html
title: Security for Humans
summary: The last thing you want to do is demonize your users. This only sets the stage for a security cold war. Instead, shift the burden to design-time. Find ways to defend against threats without hamstringing your users, and they will love you for it.
tags: [security]
---

Lately I've been thinking about an interesting interplay between a person’s:

* Desire to be productive (D)
* Appreciation for security (S)
* Faith in those who are implementing security measures (F)
* Pain threshold for said security measures (T)

Where an individual's security threshold is equal to some measure of the other three:

    T = S + F - D

When designing any system, the amount of pain (degradation to the user's experience) caused by security controls is simply the sum of the parts:

    P = sum(pain(c) for c in controls)

Ideally, we want to create systems where the pain introduced by security controls does not exceed the threshold of its users:

    P <= T

It's tempting to become fixated on the right side of the equation. "The problem is the users."  Why? Because reducing (P) is hard. It requires taking the time to do thorough risk analysis. You have to get creative with the architecture. You may have to ask for funding. Not to mention, you often have to collaborate across organizational and functional boundaries to get the job done.

I don't mean to say that working on (T) is completely wrong; in fact, you really should strive to engender a healthy understanding of&mdash;and appreciation for&mdash;security in your community (be it internal or external), working to build relationships of trust between those implementing security measures and those affected by those measures. My point is that you need to work on (P) at least as much, if not more, than (T). The problem with betting too much on (T) is that it lies in the realm of culture. Changing culture is a slow and difficult process. And if you push too hard, your efforts always backfire. 

The last thing you want to do is demonize your users. This only sets the stage for a security cold war. Instead, shift the burden to design-time. Find ways to defend against threats without hamstringing your users, and they will love you for it.
