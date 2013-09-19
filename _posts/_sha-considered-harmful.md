---
layout: post.html
title: "SHA Snake Oil"
summary: The SHA message-digest algorithm has its uses, but password hashing isn't one of them.
tags: [Security]
id: 66fc67fe-1cb7-11e3-95e0-ea6628d43830
---

High-profile breaches over the past couple of years have brought to light two inconvenient truths:

#. Securing the perimeter is no longer good enough.
#. Most software developers are naive when it comes to security<sup><a name="id-1" href="#id-1.ftn">1</a></sup>.

Many web services, as it turned out, have been storing their user's passwords in plaintext. Slightly less embarrassing to our profession&em;but still troubling&em;was the revelation that MD5 is still in wide-spread use despite it having been cracked long ago. This is all very serious stuff, especially considering that most humans reuse the same password everywhere they go.

You already knew all that. But here's the rest of the story.

Sparked by these highly-publicized breaches, a movement began to migrate away from storing plaintext and MD5-hashed passwords. The movement had the right spirit, just not the right direction. I'm not sure how this got started, but using salted, SHA-based password hashes was promulgated as the de facto "fix" for mitigating these sorts of attacks.

# SHA Snake Oil #

Here's the problem: SHA, just like MD5, is actually *optimized* for speed. In other words, just like MD5, SHA was designed to generate a one-way hash *as quickly as possible*. This is a good property to have in some cases, but when it comes to password hashing, the last thing you want is an algorithm designed for efficiency, especially in today's world of commodity GPUs that can perform **billions of hashes** per second. Armed with a video card (or two) and some knowledge of how humans typically choose passwords, it becomes trivial for an attacker to crack large portions of your average hash file.

# KDF to the Rescue! #

Key derivation functions (KDFs) comprise a family of algorithms for generating password hashes. Unlike message-digest algorithms such as MD5 and SHA, KDFs are designed to be *inefficient*. Proper use of a KDF helps to make brute-force attacks impractical to execute, in terms of cost and time, while still being fast enough that users won't notice a delay when signing in.

Here are my (current) go-to KDFs:

#. PBKDF2-HMAC-SHA256. This RSA-developed, NIST-recommended algorithm has been widely used and vetted by cryptographers. You can find it in anything from LastPass to Django, Mountain Lion to Android. PBKDF2 is a good choice if an scrypt library is not available for your programming language.
#. scrypt. This KDF is relatively new and not as battle-tested as some older algorithms, but has the advantage of requiring lots of memory, which mitigates attacks that rely on custom hardware. scrypt was invented by cryptographer Colin Percival, and is on track to becoming an IETF standard.

Personally, I think scrypt is the way to go if you can use it in your environment<sup><a name="id-2" href="#id-2.ftn">2</a></sup>. That being said, I'm not a cryptographer; you should make your own evaluation, including chatting with your friendly neighborhood security geek, before settling on any kind of security scheme for your own projects. Getting security right is really hard, and so it is always prudent to seek out advice from folks who live and breath this stuff.

@kgriffs

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup>No offense, it's just the truth.
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup>Implementations of scrypt are not as widely available as compared to PBKDF2, at the time of this writing.
  </li>
</ul>
