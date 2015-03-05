Sometimes you just need some random bits (why?). It's pretty easy to just grab some from `dev/urandom`, but what if you need a string? (why?)

http://www.2uo.de/myths-about-urandom/

This is interesting (talk about different CLI tools used)

```shell
#!/usr/bin/env bash
 
RAND_STR=`cat /dev/urandom | head -c $1 | od -An -t x1 | tr -d ' '`
 
if [ -t 1 ]
then
    echo $RAND_STR
else
    echo $RAND_STR | tr -d '\n'
fi
```

And here is the python version. It works on both Python 2 and 3.

```python
#!/usr/bin/env python

import os, sys, binascii

rand_str = binascii.hexlify(os.urandom(int(sys.argv[1]))).decode()

if sys.stdout.isatty():
    print(rand_str)
else:
    sys.stdout.write(rand_str)
```