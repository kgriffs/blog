

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

Many web services, as it turns out, store their user's passwords in plaintext. Slightly less embarrassing&em;but still troubling&em;was the revelation that MD5 is still in use despite it having been cracked long ago. This is all very serious stuff, considering that people often reuse passwords across multiple services.

Following these highly-publicized breaches, a movement began to migrate away from storing plaintext and MD5-hashed passwords. The movement had the right spirit, just not the right direction. I'm not sure how this got started, but using salted, SHA-based pasword hashes was promulgated as the de-facto "fix" for mitigating these sorts of attacks in the future.

# Missed Opportunity #

Here's the problem: SHA, just like MD5, was actually *optimized* by it's inventors for speed. In other words, these hash functions were designed to generate a one-way hash *as quickly as possible*. This is bad news in today's world of commodity GPUs that can literally hash **billions of passwords** per second. Armed with a video card (or two) and some knowledge of how humans typically choose passwords, it's trivial for an attacker to crack most of a hash file once they get their hands on it.

What should have been promoted instead?

When it comes to authenticating passwords, what you need is a good, battle-tested key-derivation function (KDF). These things are generally designed to be slow as tar. The better the KDF, the more expensive it would be for an attacker to crack a password, even if the algorithm were implemented in hardware. You basically have three choices today:

#. PBKDF2-HMAC-SHA256. This RSA-developed, NIST-recommended algorithm has been widely used and studied. You can find it in anything from LastPass to Django, Mountain Lion to Android.
#. bcrypt. Originally
#. scrypt. New, very promising, not as battle-tested as the rest, on track to becoming an IETF standard.

with all of these, can determine how slow. Benchmark it, then double the number of rounds. Make it as slow as you can without imparing usability, to gaurd against advances in hardware and cryptanalysis.

1. Plaintext scare caused people to start doing salted hashes. this was
falsley promulgated as the best practice.
2. More recent attacks are starting to wake people up to the fact that what
they thought was a best practice isnt.
3. What *is* the best practice?

references to stories, best practices

http://www.tarsnap.com/scrypt/scrypt.pdf
http://arstechnica.com/security/2013/04/why-livingsocials-50-million-password-breach-is-graver-than-you-may-think/
http://arstechnica.com/security/2012/10/sha1-crypto-algorithm-could-fall-by-2018/
http://arstechnica.com/security/2012/08/passwords-under-assault/