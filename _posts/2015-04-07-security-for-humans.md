---
layout: post.html
title: Security for Humans
summary: Don't demonize your users. This only sets the stage for a security cold war. Instead, shift the burden to design-time. Find ways to defend against threats without hamstringing your users, and they will love you for it.
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

It's tempting to become fixated on the right side of the equation, i.e., "the users are the problem."  Why? Because reducing (P) is hard. It requires formal threat modeling, creative architecture, and sufficient funding.

I don't mean to say that working on (T) is completely wrong; in fact, you should absolutely strive to engender a healthy appreciation for security, and work to build relationships of trust between those implementing security measures and those affected by said measures. However, to be successful you'll need to dig in and get to work on (P) as well. The problem with betting too much on (T) is that it lies in the realm of culture. Changing culture is a slow and difficult process. And it's a process that can easily backfire.

Don't demonize your users. This only sets the stage for a security cold war. Instead, shift the burden to design-time. Find ways to defend against threats without hamstringing users, and they will love you for it.

