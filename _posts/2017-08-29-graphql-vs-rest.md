---
layout: post.html
title: "GraphQL vs. REST"
summary: "Comparing GraphQL to REST is like comparing apples and oranges. But let's do it anyway."
tags: [code]
---

Since kicking off a new project for my startup, I've been looking into GraphQL vs. REST.

First of all, it's important to note that REST is a comprehensive _architectural style_, not a protocol. And I don't think this is really a debate about whether to use one or the other. We'll need both for the foreseeable future.

GraphQL really shines only as long as you are only talking about rich read-only data APIs. It really can be quite elegant. GraphQL does support mutations as well, but they are essentially just a way of tacking on RPC calls. Some devs think this is the bee's knees, but that's because they never really understood REST in the first place. They've never moved past thinking in terms of RPC or CRUD, but just using HTTP verbs instead of method names. 

Case in point: we tend to write RPC-style clients for REST APIs, and then proceed to complain about REST not being a useful architectural style. It's a self-fulfilling prophecy.

So of course they are excited to have somewhere else to go. 

That's not to say GraphQL is devoid of attractive qualities. Especially if you don't try to use it to mutate state. 

With GraphQL you can potentially reduce the number of calls to your API, conserve bandwidth, and improve client responsiveness. On the other hand, GraphQL may make it harder for the server to effectively cache responses, since different clients can query for wildly different data sets.

[GitHub makes some reasonable justifications](https://githubengineering.com/the-github-graphql-api/) for moving to GraphQL in the latest version of their API. On the other hand, note how they appeal to their own authority as API experts to convince you that you should trust them. Maybe. Just remember, do your own homework. **#youarenotgithub** **#youarenotfacebook**

You can do some things in REST to alleviate the pain points that GitHub mentions (ala OData, API Chaining). But the GraphQL declarative style is perhaps more elegant. On the other hand, if REST clients and APIs were to make better use (or any use at all) of caching headers and [HATEOS](https://github.com/mikestowe/cphl), this would be less of an issue. Performance would be improved, and REST clients would become far less brittle. 

Anyway, we are still climbing the hype curve on this one. We'll see how it turns out.

Further reading:

* [GraphQL (Official Site)](http://graphql.org)
* [The GitHub GraphQL API](https://githubengineering.com/the-github-graphql-api/)
* [Just Because Github Has a GraphQL API Doesn’t Mean You Should Too](https://www.programmableweb.com/news/just-because-github-has-graphql-api-doesn’t-mean-you-should-too/analysis/2016/09/21)
* [I Like GraphQL (Gist)](https://gist.github.com/skanev/f3468e8b85a3d6bc16c7aa493229eda7)