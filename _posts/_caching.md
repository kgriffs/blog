The original creator of CouchDB left the project to do CouchBase. Basically, it's a version of CouchDB "that scales". I'm not a fan of CouchDB personally, and CouchBase looks like it brings with it a lot of CouchDB baggage. Personally, I don't think the world needs another MongoDB. 

Case in point: A lot of Node.js guys use CouchDB, but they wouldn't be caught dead without Redis caching their objects.

If you want to get rid of memcached, here are my top 2 picks:
Redis, using client-side sharding. Insanely fast, very similar to memcached in that it's basically a giant hash table. Plus, 2.6 has "stored procedure" support via Lua.
MongoDB. 2.2 introduced a TTL feature, so you can now use Mongo as a cache without having to run a cron job to cull expired documents. Not quite as fast as Redis, but competitive. The plus here is we already have experience with it, and it does server-side sharing. Probably overkill for a memcached replacement, since all you really need is a hash table.
Related: A cool thing we can do to reduce cache lookup time, is to do what CPUs do, and have two levels of cache (L1, L2). L1 would be a local Redis/memcached instance that is on each web head, and L2 would be a shared cache server. 
