---
layout: post.html
title: A Better uuidgen
summary: How to create a better uuidgen that works consistently across platforms and is clipboard-friendly.
tags: [security]
id: a60d0a5a-a20a-424d-87b1-6c7bbc89f5b0
---

Recently I was putting together some examples to use in a RESTful workshop, and needed to generate a bunch of UUIDs. On OS X I have a couple of options. First, there's `uuidgen`:

```bash
$ uuidgen
E4B221B0-9466-4354-8A33-5B3EB5D3ABE3
```

Under OS X, this creates a DCE version 4 (random) UUID. Under Linux, `uuidgen` also creates a random UUID by default if a strong random number generator is available; otherwise, it defaults to generating a version 1 (time + MAC) UUID. Finally, under FreeBSD, `uuidgen` generates a version 1 UUID.

The second option I have on my MBP is the OSSP `uuid` command:

```bash
$ uuid
1d98d052-c107-11e4-a360-6796fc8cedc1
```

By default, `uuid` returns a DCE version 1 (time + MAC) UUID. However, I can override this to get a random UUID, which is usually What You Want™.

```bash
$ uuid -v 4
07158102-962d-4038-a3d6-fc6428b98313
```

You can get the OSSP `uuid` tool on Linux, although it may not be installed by default in some distributions (e.g., on Arch it is only available through AUR). Regardless, `uuid` should behave the same regardless of platform.

The first problem I have is that `uuidgen` doesn't always default to a version 4 (random) UUID, depending on your platform. On the other hand, `uuid` has a consistent default, but I would argue it is the *wrong* default (version 1).

The second problem I have is that both tools output a trailing newline character. This is fine when just writing out to the console, but is less helpful when piping, say, to the clipboard:

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

Fortunately, this is easily solved with a little bash magic:

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
