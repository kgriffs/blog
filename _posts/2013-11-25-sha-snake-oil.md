---
layout: post.html
title: "SHA Snake Oil"
summary: The SHA message-digest algorithm has its uses, but it's no cure-all.
tags: [stuff]
---

Massive, highly-publicized security breaches of online services in recent years have exposed the inconvenient truth that many web services still use MD5-based password authentication, and some don't even hash passwords in the first place.

This is serious stuff, considering that people tend to reuse the same password everywhere they go. A weak service not only risks its own business and reputation, but also everyone else's.

# Naive Password Hashing #

<img class="right" src="/assets/images/sha-digest-cure.gif" width="100px" alt="Message digest algorithms such as SHA don't solve everything." />

In the wake of these attacks, a movement began<sup><a name="id-1" href="#id-1.ftn">1</a></sup> to stop storing passwords in such a blatantly insecure way. In some circles, using a simple salted SHA was promulgated as the "best practice" fix. While certainly better than storing passwords in plaintext, or hashing them with MD5, there are other, more appropriate algorithms we should be promoting instead.

Here's the problem: SHA, just like MD5, is actually *optimized* for speed. In other words, just like MD5, SHA was designed to generate a one-way hash *as quickly as possible*. This is a good property to have in some cases, but when it comes to password hashing, the last thing you want is an efficient algorithm!

Case in point: Today's commodity GPUs can perform **billions of hashes** per second<sup><a name="id-2" href="#id-2.ftn">2</a></sup>. Armed with a few video cards (or an EC2 account) and some knowledge of how humans typically choose passwords<sup><a name="id-3" href="#id-3.ftn">3</a></sup>, it becomes trivial for an attacker to crack large numbers of passwords in a surprisingly short amount of time.

# Use the Right Tool #

What we as a community *should* be promoting, instead, is the use of strong key derivation functions (KDFs).

KDFs comprise a family of algorithms for generating password hashes. They can be used for password verification, as well as for deriving limited-use keys from a master secret. Unlike message-digest algorithms, such as MD5 and SHA, KDFs are designed to be *inefficient*. Proper use of a KDF goes a long way toward making brute-force attacks impractical to execute, in terms of both cost and time.

When asking people to move away from plaintext and MD5, we should be encouraging them to use a proper KDF, not some kind of home-grown, salted SHA digest.

That way, we make the black hats sad.

<img class="block" src="/assets/images/digest-vs-kdf.gif" width="100%" alt="Use a KDF to turn a happy black hat into a sad one." />

Here are my (current) go-to KDFs:

1. **PBKDF2.** This RSA-developed, NIST-recommended algorithm has been widely used and vetted by cryptographers. You can find it in anything from LastPass to Django, OS X to Android. PBKDF2 is a good choice if an scrypt library is not available for your programming language of choice.
2. **scrypt.** This KDF is relatively new and not as battle-tested as some older algorithms, but has the advantage of requiring lots of memory to go fast, which mitigates attacks that rely on specialized hardware.

# We must do better #

Everyone has a responsibility to the broader community to defend their portion of the web. Let's ensure we are promoting *real* best practices as we work to raise the bar on computer security.

*Caveat emptor: While I care deeply about computer security and have a working knowledge of the same, I'm no cryptographer. You should definitely invest some time into making your own evaluation of KDFs, including consulting with experts in the field to fully understand their proper use.*

<ul class="footnotes">
  <li>
    <sup><a name="id-1.ftn" href="#id-1">1</a></sup>It's about time our industry got a wake up call.
  </li>
  <li>
    <sup><a name="id-2.ftn" href="#id-2">2</a></sup>With appropriate software, i.e. <a href="http://hashcat.net/oclhashcat-plus/">hashcat</a>
  </li>
  <li>
    <sup><a name="id-3.ftn" href="#id-3">3</a></sup>See also this <a href="http://www.troyhunt.com/2011/06/brief-sony-password-analysis.html">password analysis</a>.
  </li>
</ul>
