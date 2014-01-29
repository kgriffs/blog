I'm pretty proud of the new Falcon 0.1.8 release; thanks to the hard work of our fine community of contributors, we were able to ship several frequently-requested features, including request sinks, improved uri decoding, and custom error handlers. There was also a significant amount of work done to improve performance in hot code paths, in order to offset the extra processing that was required by the new features.

Please, take 0.1.8 for a spin and tell me what you like, what you don't, and what you would like to see in the next version. You can find me in #falconframework on freenode and @kgriffs on Twitter.

A few highlights of the 0.1.8 release:

## Custom Exception Handlers ##

May even raise HTTPError, can also catch it so you can return your
own custom responses or just raise your own MyHTTPError class directly
and add a hook to convert it to the correct response.

## Case-Insensitive Headers ##

breaking, srmock...

## Request Sinks ##

## Improved URL encoding/decoding ##

query strings now properly decoded.

UTF-8 decoding/encoding per RFC 3986

Query String, uri decoding

WSGI servers decode path, but not query string (is that correct?)

New uri module - can be used by your apps

## Improved Python 3.3 Performance ##

All frameworks slow down, but Falcon slows down the least!


