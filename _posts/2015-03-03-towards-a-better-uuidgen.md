---
layout: post.html
title: A Better uuidgen
summary: A humble suggestion for a better uuidgen that works consistently across platforms and is clipboard-friendly.
tags: [security]
id: a60d0a5a-a20a-424d-87b1-6c7bbc89f5b0
---

Recently, I put together some examples to use in a RESTful workshop, and needed to generate a bunch of UUIDs. 

On OS X I have a couple of options. First, there's `uuidgen`:

```bash
$ uuidgen
E4B221B0-9466-4354-8A33-5B3EB5D3ABE3

```

Under OS X, this creates a DCE version 4 (random) UUID. However, under FreeBSD, `uuidgen` always generates a version 1 UUID. And finally, under Linux, `uuidgen` can create either version 1 or version 4 UUIDs, but defaults to a random UUID when a high-quality RNG is available.<sup><a name="id-1" href="#id-1.ftn">1</a></sup> 

The second option I have on my MBP is the OSSP `uuid` tool. It's also available on Linux and FreeBSD:

```bash
$ uuid
1d98d052-c107-11e4-a360-6796fc8cedc1

```

By default, `uuid` returns a DCE version 1 (time + MAC) UUID. I can override this to get a random UUID, which is usually what you want:

```bash
$ uuid -v 4
07158102-962d-4038-a3d6-fc6428b98313

```

Now I have a cross-platform way to generate a version 4 UUID from the command line. Next I need to get that value into my clipboard.

## Trailing newlines with uuidgen and uuid

Both `uuidgen` and `uuid` output a trailing newline character. Now, that's fine when just displaying the UUID in a terminal, but is decidedly less helpful when piping the UUID somewhere, for example [to the clipboard][1]:

```bash
$ uuidgen | pbcopy

```

Now when I paste the copied text somewhere else, like into a JSON document, the newline messes up my formatting (yes, I know, this is all very sad.)

```json
{
    "uuid": "07158102-962d-4038-a3d6-fc6428b98313
"
}

```

## A better uuidgen

Fortunately, the problems above are easily solved with a little bash magic. The systems where I run this have CPRNGs, so I'm comfortable with forcing version 4:

```bash
#!/usr/bin/env bash

if [ -t 1 ]
then
    uuid -v 4
else
    uuid -v 4 | tr -d '\n'
fi

```

This script first tests whether output is attached to a terminal. If so, a version 4 UUID is output with a trailing newline. Otherwise, if we are piping the output, we'll strip off the trailing newline character.

Or, if you don't want to depend on OSSP's `uuid` tool:

```python
#!/usr/bin/env python

import sys
import uuid

result = str(uuid.uuid4())
if sys.stdout.isatty():
    print(result)
else:
    sys.stdout.write(result)

```

The Python `uuid.uuid4()` function will use your operating system's native `uuid_generate_random` function call, if available, to generate the UUID. Failing that, it will use `os.urandom`. Only if a CPRNG is unavailable will `uuid.uuid4()` resort to using `random.randrange(256)` like some kind of primitive animal.<sup><a name="id-2" href="#id-2.ftn">2</a></sup> 

Now I have a version of `uuidgen` that works consistently across platforms, and is pipe-able. 

Hooray!

<ul class="footnotes">
    <li>
        <sup><a name="id-1.ftn" href="#id-1">1</a></sup>I suppose this makes some kind of sense, since a bad generator would be more likely to introduce collisions. You also don't want to lull the user into a false sense of security (allowing them to assume their UUIDs are unpredicatable and opaque when they actually aren't).
    </li>
    <li>
        <sup><a name="id-2.ftn" href="#id-2">2</a></sup>If you have to use such a platform, you have my sympathy.
    </li>  
</ul>

[1]: http://stackoverflow.com/questions/749544/pipe-to-from-clipboard

