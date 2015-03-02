http://lists.openstack.org/pipermail/openstack-dev/2015-February/056968.html

None of the options described in the post above follow the uniform interface constraint. They all invent domain-specific actions. Instead of approaching the problem from an RPC mindset (actions and endpoints), they should be thinking more in terms of dereferencing links provided by the server to change the state of resources.

RPC relies on out-of-band definitions of semantics, rather than letting the resource representations and standard HTTP methods describe the interaction. This makes it harder for clients and servers to evolve independently. Put another way, it makes it more difficult to modify the API in the future without breaking clients.

[what are some examples of breaking changes? then counter example showing how REST helps]


PUT /images/{image_id}/active

{
    "active": true
}


PATCH /images/{image_id}

[
    { "op": "replace", "path": "/active", "value": true }
]

