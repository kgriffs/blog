Heh, funny you mention that. Colin has a bad habit of trolling the internet in the interest of promoting his own startup. He caused quite a PR nightmare for us a year or two ago re JD crypto. Some of his points were valid, some were based on invalid assumptions about our code, but overall he isn't exactly known for tact.

In any case, we can look at using scrypt, although I tend to lean on stuff that has been more battle-tested. I'd be willing to bet more cryptographers have beat on PBKDF2 in the last few years than scrypt. Plus, we are using a huge number of rounds, and an attacker would have to repeat those 10,000 rounds for every single block of data we back up. 

That being said, I like the idea of scrypt requiring lots of memory. We might consider it for a future RCBU cipher version in a few years, once it's been released to the wild and been more widely proven.

P.S. - On the subject of alternatives to RSA-designed algorithms, ECC is pretty sweet. However, it hasn't seen widespread use, so we stuck with RSA-2048. If nothing else, you're less likely to find bugs in RSA libraries than in ECC ones, since the squeaky wheel gets the grease.

To supplement Kurt's tech talk, I know of a few free courses that cover cryptography at length:

Udacity's:
- Applied Cryptography: http://www.udacity.com/overview/Course/cs387/CourseRev/apr2012

Coursera's:
- Cryptography I: https://www.coursera.org/course/crypto
- Cryptography II: https://www.coursera.org/course/crypto2
