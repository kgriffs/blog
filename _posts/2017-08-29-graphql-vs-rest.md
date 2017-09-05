---
layout: post.html
title: "GraphQL vs. REST"
summary: "Comparing GraphQL to REST is like comparing apples and oranges. But let's do it anyway."
tags: [code]
---

Since kicking off a new project for my startup, I've been looking into GraphQL vs. REST.

First of all, it's important to note that GraphQL is just for read-only APIs. You still need some other mechanism for updating resources. Also note that REST is a comprehensive _architectural style_, not a protocol. So this isn't really a debate about whether to use one or the other. We'll need both for the foreseeable future.

That being said, there are a great many devs who never really understood REST (still thinking in terms of RPC or CRUD, but just using HTTP verbs instead of method names) and are excited to have somewhere else to go. We tend to write RPC-style clients for REST APIs, and then proceed to complain about REST not being a useful architectural style. It's a self-fulfilling prophecy.

So it's important to not conflate GraphQL (or REST) with RPC. Better to judge them on their own merits rather than squinting at them through a dirty lens.

GraphQL does have some attractive qualities. It's not really RPC-over-HTTP, more like read-only-SQL-over-HTTP, but decoupled from the backend data model. So I suppose it is better than what has been tried before. 

With GraphQL you can potentially reduce the number of calls to your API, conserve bandwidth, and improve client responsiveness. That being said, GraphQL may make it harder for the server to effectively cache responses, since different clients can query for wildly different data sets.

[GitHub makes some reasonable justifications](https://githubengineering.com/the-github-graphql-api/) for moving to GraphQL in the latest version of their API. On the other hand, note how they appeal to their own authority as API experts to convince you that you should trust them. Maybe. Just remember, do your own homework. **#youarenotgithub** **#youarenotfacebook**

You can do some things in REST to alleviate the pain points that GitHub mentions (ala OData, API Chaining). But the GraphQL declarative style is perhaps more elegant. On the other hand, if REST clients and APIs were to make better use (or any use at all) of caching headers and [HATEOS](https://github.com/mikestowe/cphl), this would be less of an issue. Performance would be improved, and REST clients would become far less brittle. 

Anyway, we are still climbing the hype curve on this one. We'll see how it turns out.

Further reading:

* [GraphQL (Official Site)](http://graphql.org)
* [The GitHub GraphQL API](https://githubengineering.com/the-github-graphql-api/)
* [Just Because Github Has a GraphQL API Doesn’t Mean You Should Too](https://www.programmableweb.com/news/just-because-github-has-graphql-api-doesn’t-mean-you-should-too/analysis/2016/09/21)
* [I Like GraphQL (Gist)](https://gist.github.com/skanev/f3468e8b85a3d6bc16c7aa493229eda7)