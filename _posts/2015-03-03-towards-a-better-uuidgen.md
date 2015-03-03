---
layout: post.html
title: Toward A Better uuidgen
summary: A humble suggestion for a better uuidgen that works consistently across platforms and is clipboard-friendly.
tags: [security]
id: a60d0a5a-a20a-424d-87b1-6c7bbc89f5b0
---

## A UUID adventure

Recently I was putting together some examples to use in a RESTful workshop, and needed to generate a bunch of UUIDs. On OS X I have a couple of options. First, there's `uuidgen`:

```bash
$ uuidgen
E4B221B0-9466-4354-8A33-5B3EB5D3ABE3
```

Under OS X, this creates a DCE version 4 (random) UUID. However, under FreeBSD, `uuidgen` always generates a version 1 UUID. And finally, under Linux, `uuidgen` can create either version 1 or version 4 UUIDs, but defaults to a random UUID when a decent RNG is available. I suppose this makes some kind of sense, since a bad generator would be more likely to introduce collisions.

The second option I have on my MBP is the OSSP `uuid` command. This should work the same on all platforms:

```bash
$ uuid
1d98d052-c107-11e4-a360-6796fc8cedc1
```

By default, `uuid` returns a DCE version 1 (time + MAC) UUID. However, I can override this to get a random UUID, which is probably What U Want™.

```bash
$ uuid -v 4
07158102-962d-4038-a3d6-fc6428b98313
```

You can get the OSSP `uuid` tool on Linux, although it may not be installed by default in some distributions (e.g., on Arch it is only available through AUR).

## Reconciling uuidgen and uuid

Now, the first problem I have with the status quo is that `uuidgen` doesn't always output a version 4 (random) UUID, depending on your platform. On the other hand, `uuid` does have a consistent default, but it is arguably the *wrong* default (version 1).

## Piping UUIDs

The second problem I have is that both tools output a trailing newline character. Now, that's fine when just writing out to the console, but is decidedly less helpful when piping, say, to [the clipboard][1]:

```bash
$ uuidgen | pbcopy
```

When I paste the copied text somewhere else, like into a JSON document, the newline messes up my formatting. Booh!

```json
{
    "uuid": "07158102-962d-4038-a3d6-fc6428b98313
"
}
```

## A better uuidgen

Fortunately, the problems above are easily solved with a little bash magic. The systems I run this on have good random pools, so I'm comfortable with forcing version 4:

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

Now we have a version of `uuidgen` that works consistently across all platforms, and is clipboard-friendly. Hooray!

[1]: http://stackoverflow.com/questions/749544/pipe-to-from-clipboard