
Using limit and marker query parameters is pretty common, so it makes sense to support those for the sake of consistency, regardless of whether we offer a way to perform ad-hoc queries. 
If we want to support ad-hoc queries, it would be best to use something that's already standardized. As Jay proposed, APIs could implement a subset of OData operators, such as $filter, $select, $top, $skiptoken, and $orderby. The dollar-sign prefix makes it easy for the server to distinguish between a simple queries and an ad-hoc one.
Ad-hoc queries encourage clients to treat  a service as a database. This behavior can kill performance and create a leaky API abstraction. That being said, you can mitigate performance degradation by running something like Lucene in parallel to a service's primary DB. 
As an alternative to completely ad-hoc queries, we can try making simple queries more flexible, by supporting a few more parameters:
sortbyAsc and sortbyDesc (e.g., sortbyAsc=name)
fields (e.g., fields=name,email)
{field}={value} (e.g., name=miles%20davis&email=miles@example.com)


Following up on #4 (below), the {field}={value} query style would limit us to "name1 == "value1" AND "name2" === "value2" queries. The OData $filter is much more flexible, allowing us to (optionally) support additional operators such as OR, !=, <, >, etc. 

If we limit OData in our APIs to only a subset of $filter operators, we are no longer allowing arbitrary SQL-like queries, which makes me a lot more comfortable with the proposal. However, I still like the idea of using a search-optimized data store ala Lucene for all OData-style queries.

An API might start by supporting only the following $filter operators:

eq
and

Later, if there's demand for it, the API could add a few more:

or
ne

Just thinking out loud here…
 
…but when we start getting into the lucene style queries, I wonder if that fits into the Search as a service (is this Stretch?).  Maybe have products send/update and index searchable data to the Search service rather than having each product build their own lucene engines?  That way we can maybe build search and filtering across all cloud products, and reach wouldn’t have to make 20 different api calls when searching for generic terms (eg tags) across all products.
