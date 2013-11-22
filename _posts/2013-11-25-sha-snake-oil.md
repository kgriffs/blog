---
layout: post.html
title: "SHA Snake Oil"
summary: The SHA message-digest algorithm has its uses, but password hashing isn't one of them.
tags: [Security]
id: 66fc67fe-1cb7-11e3-95e0-ea6628d43830
---

Massive, highly-publicized security breaches of online services in recent years have exposed the inconvenient truth that many web services still use MD5-based password authentication, and some don't bother to hash passwords in the first place.

This is serious stuff, considering how people tend to reuse the same password everywhere they go. Every software developer must be vigilant in defending their section of the wall. A weak service not only risks its own business, but also everyone else's.

# Naive Password Hashing #

In the wake of these breaches, a movement began<sup><a name="id-1" href="#id-1.ftn">1</a></sup> to stop storing passwords in such a blatantly insecure way. In some circles, using a simple salted SHA was promulgated as the "best practice" fix. While certainly better than storing passwords in plaintext or hashing them with MD5, there are other algorithms purpose-made for this sort of thing which are far more secure.

If we as an industry agree there is a critical need to change the status quo, we should not squander the opportunity by recommending a naive, short-term fix.

Here's the problem: SHA, just like MD5, is actually *optimized* for speed. In other words, just like MD5, SHA was designed to generate a one-way hash *as quickly as possible*. This is a good property to have in some cases, but when it comes to password hashing, the last thing you want is an algorithm designed for efficiency!

Case in point: Today's commodity GPUs can perform **billions of hashes** per second<sup><a name="id-2" href="#id-2.ftn">2</a></sup>. Armed with a few video cards (or an EC2 account) and some knowledge of how humans typically choose passwords<sup><a name="id-3" href="#id-3.ftn">3</a></sup>, it becomes trivial for an attacker to crack large numbers of passwords in a surprisingly short amount of time.

# Use the Right Tool #

What we as a community *should* be promoting, instead, is the use of strong key derivation functions (KDFs).

KDFs comprise a family of algorithms for generating password hashes. They can be used for password verification, as well as for deriving limited-use keys from a master secret. Unlike message-digest algorithms, such as MD5 and SHA, KDFs are designed to be *inefficient*. Proper use of a KDF goes a long way toward making brute-force attacks impractical to execute, in terms of both cost and time.

Here are my (current) go-to KDFs:

1. **PBKDF2.** This RSA-developed, NIST-recommended algorithm has been widely used and vetted by cryptographers. You can find it in anything from LastPass to Django, OS X to Android. PBKDF2 is a good choice if an scrypt library is not available for your programming language of choice.
2. **scrypt.** This KDF is relatively new and not as battle-tested as some older algorithms, but has the advantage of requiring lots of memory to go fast, which mitigates attacks that rely on specialized hardware.

Caveat emptor: while I do care deeply about computer security and have a working knowledge of the same, I'm not a cryptographer. You should definitely invest some time into making your own evaluation, including consulting with security experts in the field.

# We must do better #

Everyone has a responsibility to the broader community to defend their portion of the web. Let's ensure we are promoting *real* best practices as we work to raise the bar on computer security.

@kgriffs

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup>Perhaps due to the scale of the security breaches and their wide coverage in the media. In any case, it's about time our industry got a wake up call!
  </li>
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup>With appropriate software, i.e. <a href="http://hashcat.net/oclhashcat-plus/">hashcat</a>
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup>For example, see <a href="http://www.troyhunt.com/2011/06/brief-sony-password-analysis.html">this password analysis</a>.
  </li>
</ul>
