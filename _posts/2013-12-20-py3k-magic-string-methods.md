---
layout: post.html
title: "Painless Py3K Unicode Magic"
summary: Implementing Python's magic string methods is tricky when it comes to Unicode characters and Py3K compatibility. I recently came across this problem in OpenStack, and wanted to share the strategy we are using to work around the issue.
tags: [code]
id: 86f0c668-676c-11e3-9218-5f2528d4383
---

Implementing Python's magic string methods is tricky when it comes to Unicode characters and Py3K compatibility. If your strings contain non-ASCII characters, ostensibly innocent statements such as `str(thing)` blow up without warning. I recently came across this problem in OpenStack, and wanted to share the strategy we are using to work around it.

The first step is to standardize on wide strings throughout your code base, only converting to UTF-8 byte strings at the edges, when it is required to communicate with the outside world. This strategy minimizes the number of places text encoding bugs can hide.

Next, once you have normalized your code to use `six.text_type` in lieu of `str`, find everywhere  you use string coercion. You will want to change all the expressions that look like this:

```python
str(thing)
```

to this:

```python
six.text_type(thing)
```

Finally, if you ever override the default magic string methods, you will need to do something like this ([gist](https://gist.github.com/kgriffs/7951625)):

```python
import six

class FooError(Exception):

    message = u'An unknown exception occurred.'

    # Called under both Py2 and Py3K for str(ex)
    def __str__(self):
        if six.PY3:
            return self.message

        # Avoid UnicodeDecodeError in py2 when the string
        # contains non-ASCII characters.
        return self.message.encode('utf-8')

    # Called under Py2 for unicode(ex) and ignored in Py3
    def __unicode__(self):
        return self.message


# elsewhere...

def do_something():
    raise FooError()

try:
    do_something()
except FooError as ex:
    # Returns a UTF-8 string in py2, and a wide string in py3,
    # both of type `six.text_type`, with no coercion. Normally you
    # would use `six.text_type` instead (see below)
    msg_a = str(ex)

    # Returns `unicode` in py2 and `str` in py3.
    msg_b = six.text_type(ex)
```

The result of `__str__` under Py2 is always coerced to `str` when `unicode` is returned, which results in an ugly `UnicodeDecodeError` when the string contains non-ASCII code points:

```pycon
>>> class BadLlama(object):
...     def __str__(self):
...         return u'€'
...
>>> badness = BadLlama()
>>> str(badness)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character u'\u20ac' in position 0: ordinal not in range(128)
>>>

```

Happy Hacking!

@kgriffs

<br>