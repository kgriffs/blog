On the other-other hand, this looks pretty sweet:

http://www.rackspace.com/cloud/public/loadbalancers/technology/

If needed, we could DNS-RR to scale out the SSL-ness.


http://hezmatt.org/~mpalmer/blog/2011/06/28/ssl-session-caching-in-nginx.html
http://vincent.bernat.im/en/blog/2011-ssl-benchmark.html
https://github.com/bumptech/stud
http://haproxy.1wt.eu/#secu

Thanks guys for the insights. At the OpenStack Summit I went to several security-related sessions and one thing that was discussed was using SSL even internal to the cluster, rather than terminating at the edge as is currently done with OpenStack deployments. This is very helpful from a security perspective, so if we can figure out a fairly painless way of doing it, I would prefer going that route.

Keep in mind that recent CPUs give you encryption mostly for free (assuming we only allow AES), and you can workaround negotiation latency via shared session caches (available in both stud and nginx).

On Oct 17, 2012, at 10:05 AM, Martin Burolla <martin.burolla@rackspace.com>
 wrote:

Here’s my humble opinion on the Windows side.
 
Quattro uses SSL termination on the load balancer.  Jungle Disk uses SSL termination on the web server.  SSL termination on the load balancer is better than SSL termination on the web server for the following reasons:
 
1)      Easier maintenance – It’s much easier to update one cert on a load balancer vs. updating a cert on every web server.   Strangely, with Jungle Disk updating a cert for one website can break the bindings on another website running on the same box.  This happens about 50% of the time and I absolutely hate it (IIS 7.0).  As a result, whenever I update a cert on a box, I have to test (and possibly fix) the bindings on the other sites.  PITA. 
 
2)      Hardware acceleration –F5 load balancers have dedicated hardware to handle the decryption and encryption.  However, I heard the new Dell 710 servers now have dedicated hardware to handle SSL traffic.  But I’m willing to bet F5 does it better.  That’s their business, that’s what they do, let them do it.
 
3)      Just makes sense – If your web server does not have dedicated SSL hardware, you’re going to waste precious CPU ticks processing SSL packets on your box.  Shouldn’t your web server be solely focused on making your app kick ass? 
 
4)      PCI compliance – Suppose you want to implement a Web Application Firewall (WAF) in your production cluster?  According to the Rackspace PCI compliance team, a WAF should be placed after an SSL terminated load balancer.  A WAF can’t process encrypted traffic.  We can’t install a WAF with the current Jungle Disk configuration.
 
Thanks,
Marty
 
From: Roger D. Farmer [mailto:roger.farmer@mailtrust.com] 
Sent: Tuesday, October 16, 2012 20:46
To: Kurt Griffiths
Cc: devops.atl@lists.rackspace.com; Jamie Painter
Subject: Re: [devops.atl] SSL termination
 
This is what I love about my job...
 
Specifically in our case as in many cases we host several websites per server to support our product. The result is that we concurrently handle the accumulated traffic of all our sites on each web server.  At peak time this can reach and exceed five-digit numbers per second.  The load introduced in encrypting this scale of traffic is literally overwhelming to the server. It is a HUGE computationally expensive task.
 
What should happen is we architect our environment to use small, specialized services, one server one task.  Just like programming, keeping things compartmentalized reduces administration cost and it's a whole lot easier to scale where necessary.
 
Ideally (most major companies) use unix to proxy incoming connections, depending on the scale, the proxy does the SSL offloading for there backend web services.  Products like Pound and Nginx can proxy and support SSL with minimal cpu load freeing up web servers to do what they do best.
 
This is just a few points, I could go on and on.  To be totally honest I can NOT come up with one good reason to support SSL on the web server, if you can I would love to hear it.  If you would like to have a detailed discussion on this I would be more than happy to give you real world insight on the topic from an engineers perspective.
 
(whispers) Just as an added note, Microsoft uses unix proxies to handle there SSL :)
 
 
Roger D. Farmer

Systems Engineer
Rackspace | Cloud

Email: roger.farmer@rackspace.com
Web: http://www.rackspace.com/cloud

"Try not to become a man of success but rather to become a man of value" Albert Einstein (1879 - 1955)


-----Original Message-----
From: "Kurt Griffiths" <kurt.griffiths@rackspace.com>
Sent: Tuesday, October 16, 2012 6:18pm
To: "Roger Farmer_Mailtrust" <roger.farmer@mailtrust.com>
Cc: "devops.atl@lists.rackspace.com" <devops.atl@lists.rackspace.com>, "Jamie Painter" <jamie.painter@rackspace.com>
Subject: Re: [devops.atl] SSL termination

Why is terminating on the web servers so bad?
 
On Oct 16, 2012, at 12:34 PM, Roger D. Farmer <roger.farmer@mailtrust.com> wrote:
 
YES YES YES!!!  SSL termination on web servers is BAD!!!  We should 100% offload SSL on the load balancer or proxy solution.
 
Roger D. Farmer

Systems Engineer
Rackspace | Cloud

Email: roger.farmer@rackspace.com
Web: http://www.rackspace.com/cloud

"Try not to become a man of success but rather to become a man of value" Albert Einstein (1879 - 1955)


-----Original Message-----
From: "Kurt Griffiths" <kurt.griffiths@rackspace.com>
Sent: Tuesday, October 16, 2012 2:51pm
To: "devops.atl@lists.rackspace.com" <devops.atl@lists.rackspace.com>, "Jamie Painter" <jamie.painter@rackspace.com>
Subject: [devops.atl] SSL termination

Hi guys,
What are you thoughts on terminating SSL at the LB vs. on the individual api servers? In order to scale-out SSL and improve inter-cluster security, it seems to make the most sense to use something like stud on each web head, with a shared session cache.
Alternatively, we could create an SSL offloading layer (LB ==> SSL-OFF ==> APPs). I like this one less, since it adds complexity and you loose traffic encryption on the last hop.
See also:
http://hezmatt.org/~mpalmer/blog/2011/06/28/ssl-session-caching-in-nginx.html
http://vincent.bernat.im/en/blog/2011-ssl-benchmark.html
https://github.com/bumptech/stud
http://haproxy.1wt.eu/#secu
Kurt
