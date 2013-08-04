

Three points:

Over the past few years we've seen a string of attacks targeting well-known web
services. The ensuing identity theft and PR nightmares prompted a migration
in the community away from naive password managmeent to what was promulgated as
a more "secure" set of best pratices. Unfortunately, this new set of practices
have been deprecated for years, but somehow everyone missed the memo.

I'm not a cryptographer, just a concerned citizen.

# Plaintext, MD5 Considered Harmful #

High-profile breaches over the past couple of years have brought to light two inconvenient truths:

#. Securing the perimiter is no longer good enough.
#. Many software developers are naive when it comes to security.

Many web services, as it turns out, store their user's passwords in plaintext. Slightly less embarrassing to us software engineers&em;but still troubling&em;was the revelation that MD5 is still in use despite it having been cracked long ago. This is all very serious stuff, especially considering that people often reuse passwords across multiple services.

Following these highly-publicized breaches, a movement began to migrate away from storing plaintext and MD5-hashed passwords. The movement had the right spirit, just not the right direction. I'm not sure how this got started, but using salted, SHA-based pasword hashes was promulgated as the de-facto "fix" for mitigating these sorts of attacks in the future.

# SHA Considered Harmful #

Here's the problem: SHA, just like MD5, was actually *optimized* by it's inventors for speed. In other words, these hash functions were designed to generate a one-way hash *as quickly as possible*. This is bad news in today's world of commodity GPUs that can literally hash **billions of passwords** per second. Armed with a video card (or two) and some knowledge of how humans typically choose passwords, it's trivial for an attacker to crack a hash file once they get their hands on it.

# KDF to the Rescue! #

When it comes to authenticating passwords, what you need is a battle-tested key-derivation function (KDF). Unlike hash functions, these KDF things are designed to run as slow as tar. When it comes to security, you don't have to be perfect, just good enough to make cracking your data more trouble than it's worth. That's exactly what a KDF is designed to do; slow down an attack just enough that it becomes impractical to execute, in terms of compute power and time, while still being fast enough that users don't notice the delay when signing in.

Choosing an aswesome KDF is pretty easy; there are really only two options you need to consider:

#. PBKDF2-HMAC-SHA256. This RSA-developed, NIST-recommended algorithm has been widely used and studied. You can find it in anything from LastPass to Django, Mountain Lion to Android. PBKDF2 is most likely available for your language of your choice.
#. scrypt. This KDF is relatively new, but has the advantage of requiring lots of memory, which mitigates custom hardware attacks. scrypt was invented by cryptographer Colin Percival, and is on track to becoming an IETF standard.

My personal recommendation would be to go with scrypt unless your programming language and/or platform does not yet support it. Keep in mind, however, that I'm not a cryptographer, so you should make your own evaluation and talk to some folks who live and breath crypto before settling on any kind of authentication scheme for your project.

references to stories, best practices

http://www.tarsnap.com/scrypt/scrypt.pdf
http://arstechnica.com/security/2013/04/why-livingsocials-50-million-password-breach-is-graver-than-you-may-think/
http://arstechnica.com/security/2012/10/sha1-crypto-algorithm-could-fall-by-2018/
http://arstechnica.com/security/2012/08/passwords-under-assault/