gtk: arc4random() is to /dev/urandom as getentropy() is to /dev/random (as far as as blocking goes). However, arc4random() was less secure in older BSDs before the switch to ChaCha20.

arc4random uses getentropy() on newer BSD when available.

https://news.ycombinator.com/item?id=8033779

arc4random() should be avoided IMO, on many systems (including OS X) it really is still arc4;

http://www.openbsd.org/papers/hackfest2014-arc4random/index.html


but what about mersene twister + dev/urandom seed? 

http://eternallyconfuzzled.com/arts/jsw_art_rand.aspx

(look at performance, need to reseed on occasion? Modern version of arc4random on freebsd is nice, but on os x still uses RC4... but still better than fallling back to rand() for GUID on Python...)