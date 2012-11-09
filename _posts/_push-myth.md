As it happens, Big Data recently kicked off development of a cloud message bus product. The product will expose a RESTful API, and will support both eventing (ala AtomHopper and RSE) and transactional semantics (ala Amazon SQS). It will be developed in the open so everyone is welcome to contribute ideas and code (stay tuned for details).

## Re Polling Architectures ##

The Rackspace Cloud Backup team has proven with RSE (and it's predecessor, PLC) that you can scale such a message bus to 100's of thousands (even millions) of clients and topics, with low latency and efficient hardware utilization.

Keys to RSE's success:

* Stateless architecture
* Polling modes (throttle up when user interaction is required, throttle down when more latency can be tolerated)
* Keep-Alive (used in conjunction with fast-poll mode, in order to achieve realtime latency (i.e., in terms of human interaction design, meaning 50 ms or less). Not used in other modes.)
* SSL session caching
* Gzip compression to minimize transport time
* Optimized web framework and server stack (currently turning requests around in 10-20 ms, in production)

<SWAG>
Based on pre-launch performance testing and live New Relic stats, RSE's current 16-box production cluster will be able to handle north of 70,000 clients, serving around 500,000 reqs/min while keeping response times under 50 ms.
</SWAG>

Stuff that could be done with RSE to further reduce latency and/or increase efficiency: 

* Response caching
* Batch posts
* Migration to PyPy (should improve throughput by at least 40%)
* Further web framework and OS tuning to reduce latency and increase efficiency
* Optimistic polling (rather than responding immediately with HTTP 204 when a topic/queue is empty, wait a moment for any messages to arrive)
* HTTP 1.1 pipelining support
* SPDY/HTTP2.0 support
* AES-NI and RdRand for speeding up SSL/TLS
* AtomNuke integration
* Geo-DNS to direct requests to the closest DC

## Mobile Notifications ##

I would like to see us offer something akin to Amazon's SNS. Such a service could act as a forwarding broker for mobile push notifications, SMS, email, web hooks, etc. Rather than tightly coupling eventing and notifications--as Amazon chose to do with SNS--our notifications service could build on our generic message bus product. Such a service could even act as a bridge to more specialized eventing systems that are optimized for single-tenant, on-the-LAN use cases.

On 10/26/12 3:06 PM, "Bryan Taylor" <btaylor@rackspace.com> wrote:

Is PubSubHubBub able to reach mobile devices directly?

On 10/26/2012 01:24 PM, Adrian Otto wrote:
I agree with both Paul and Greg on this subject. Pull (poll) and Push (event callback) notifications are both useful, and each are suitable for different types of use cases. Using either of them the wrong way can be very bad, particularly at scale.

We should have well standardized and well socialized solutions for both types of messaging. It's probably a mistake to try and offer solutions for both types of messaging in a single service. These are different animals with very different server implementation needs. My suggestion is to see about using PubSubHubBub in combination with Atom Hopper on a short term basis while a really solid, standards based push notification solution can be offered as an alternative. Implementers of PubSubHub should be required to abstract their implementations such that they can be easily adjusted later to use an alternate pub/sub and message queuing service.

  From my perspective, an ideal solution would support ATOM for the use cases that Atom Hopper is suitable for, and something AQMP compliant with a ReSTful overlay interface (designed to support large numbers of relatively long-lived HTTP connections, with a limited amount of server-side state. There should also be a simple and reliable way to bridge the two services (Push+Pull) together to support mixed use cases. This will be particularly useful for mobile for reasons already covered in this thread.

I also believe strongly that we should plan to offer these services to our customers. We are not the only ones building SOA applications that have these same needs.

Adrian

On Oct 26, 2012, at 5:26 AM, Greg Herlein <greg.herlein@RACKSPACE.COM>
   wrote:

I think polling can be a good solution for many problem patterns.
However, our experience in Reach has pointed out that issues arise when
building user interfaces or other systems where latency matters.  Whether
you want to provide feedback to the user (turn the server state icon
green, for example) or take the next step in a series of actions (add the
newly booted server to a load balancer, for example) the variable we want
to minimize is latency.  If we are polling every 10 seconds and the server
is ready at 11 seconds, the user saw an extra 9 seconds delay - and that
is perceived as 'why is this thing so slow?'  In addition, a large number
of clients polling constantly for state change does place a significant -
and non-determinstic - load on the system being polled.  This past summer
Reach had to reduce it's polling rate (thus making it's apparent
responsiveness worse) because underlying systems were getting hammered.
If those systems could distribute events to subscribed clients instead the
latency would be reduced and the processing load on the underlying system
becomes constant and predictable.

In addition, I agree that for mobile polling is very undesirable.  Every
network operation consumes battery and applications in the background may
not be able to use the network at all (or only for certain specific
things).  On iOS for example, a polling solution would not work at all
unless the app was in the foreground.  Push notifications are the only way
to 'wake up' a sleeping application.

I love these kinds of conversations.  The next time we can get a group of
interested developers together for a conversation we should.  Or better,
an internal Rackspace developer conference!  Until then I hope we can keep
this kind of thing going on the lists!



On 10/25/12 10:29 PM, "Paul Querna" <paul.querna@rackspace.com> wrote:

The architectural positives of polling are massive -- I completely
agree.  I think our core infrastructure should be based around this
kind of pattern, however for mobile applications consumers we should
definitely be open to having a second set of software that consumes
these poll based central repositories and sends push information to
mobile clients.



The affects of polling are in conflict with Mobile devices, system
software, operating environments, and desired user experiences
(extreme responsiveness).

Perhaps the best simple example is that of polling every 10 seconds
for a changes URL. (weither using ETags or not)

In a high bandwidth, low latency server environment, not only is TCP
setup "cheap", but the software stacks are even more likely to
implement HTTP Keep Alive, potentially removing TCP handshake
overheads.  A great example of this in a massive high performant
system is the Apache Kafka[1] project.

Compared this to iOS and Android[2], which HTTP Keep Alive is
basically not usable -- and you have a much harder time swapping out
the HTTP Client libraries.  Since every request means rebuilding the
connection, the latency can easily add several more seconds to the
life of every request.  Does this break the app? No, it just reduces
the perceived responsiveness.

Additionally, because your application may not even be "open", you
cannot always be able to poll for changes -- the push notification
services provided by the OS allow you to trigger interaction, to open
our application and then do work.

[1] - http://incubator.apache.org/kafka/
[2] - http://www.guypo.com/mobile/http-pipelining-big-in-mobile/

On Thu, Oct 25, 2012 at 9:50 PM, Jorge Williams
<jorge.williams@rackspace.com> wrote:
Because it means that at the server end, we don't have to maintain the
state
of our subscribers (clients maintain their own state), also we can
better
utilize caching -- we can do guaranteed delivery without a lot of the
headaches that are normally associated with it.

Checkout: http://www.infoq.com/presentations/robinson-restful-enterprise

-jOrGe W.

On Oct 25, 2012, at 11:35 PM, Greg Herlein wrote:

Why poll?  Some consider polling to be evilŠ
---
Greg Herlein
Director, Software and Product Development
Rackspace Hosting
415-368-7546
@gherlein


From: Jesse Gonzalez <jesse.gonzalez@rackspace.com>

Date: Thursday, October 25, 2012 7:17 PM
To: Paul Voccio <paul.voccio@rackspace.com>
Cc: Ed Rooth <ed.rooth@RACKSPACE.COM>, Josh Schairbaum
<josh.schairbaum@RACKSPACE.COM>, Greg Herlein
<greg.herlein@rackspace.com>,
"dev@lists.rackspace.com" <dev@lists.rackspace.com>

Subject: Re: New Mailing List: Mobile Ideas!

We just had a conversation about exposing this level of information via
ATOM
to customers, however polling would still be required.

On Oct 25, 2012, at 7:11 PM, Paul Voccio <paul.voccio@rackspace.com>
wrote:

We've talked about having a call back service when things happen on an
instance. Finished booting, state change, etc. This isn't monitoring
per se,
but implementing a hook that can notify when something happens at the
control plane. A notification on a mobile without polling for this
would be
spiffy.


Thanks,
pvo
--
Paul Voccio
paul.voccio@rackspace.com
770-335-2143(c)
pvo on #openstack

From: Ed Rooth <ed.rooth@rackspace.com>
Date: Thursday, October 25, 2012 5:39 PM
To: Josh Schairbaum <josh.schairbaum@RACKSPACE.COM>, Greg Herlein
<greg.herlein@RACKSPACE.COM>, "dev@lists.rackspace.com"
<dev@lists.rackspace.com>
Subject: Re: New Mailing List: Mobile Ideas!

Other than the at-a-glance view, I think the most useful mobile features
would be alerts. Monitoring alerts are obvious, but also billing
threshold
alerts, and support ticket related alerts.

Oh, and super obvious and simple, but a big prominent button to dial
Rackspace support would be nice.

Ed



On Thu, Oct 25, 2012 at 3:15 PM, Brad Gignac <brad.gignac@rackspace.com>
wrote:
I'd love for the mobile app to really focus on monitoring and
visualization. If I'm doing infrastructure work, I'll probably use
Chef or
possibly the web UI. On my phone, I'd really like good at-a-glance
information about my infrastructure.

-Brad

________________________________
From: Josh Schairbaum [josh.schairbaum@rackspace.com]
Sent: Thursday, October 25, 2012 6:04 PM
To: Greg Herlein; dev@lists.rackspace.com
Subject: Re: New Mailing List: Mobile Ideas!

I think it would be awesome if the new Rackspace Cloud control panel
worked well on an iPhone/iPad. While trying to provision a server last
week
I ran into the following problems:
* cannot copy and paste API key
* cannot copy and paste root password
* hard to navigate with the javascript drop downs
* impossible to scroll when zoomed in

I know there's a mobile app that only requires username & password,
but on
a fresh iPad I got confused between the 2 versions available. It was a
fairly frustrating 15 minutes as I tried to provision and log in to a
new
cloud server. I think a great start would be tightening up existing
apps.

JS

From: Greg Herlein <greg.herlein@rackspace.com>
Date: Thursday, October 25, 2012 12:25 PM
To: "dev@lists.rackspace.com" <dev@lists.rackspace.com>
Subject: New Mailing List: Mobile Ideas!

Hello everyone!  We are starting to get more serious about our mobile
development efforts.  Among this will be updating our existing mobile
apps,
developing a new mobile Cloud Monitoring app, work on mobile
development
SDKs, and working to make it super easy for mobile developers to use
the
Open Cloud.

Out here in San Francisco there's a common feel that the only two hot
technologies right now are cloud and mobile ­ and that the two need
each
other!  This merge of technologies is changing everything ­ and will
keep
changing everything.  But we need your good ideas!  Rackers know best
what
kind of great things we can do to help our customers.  So please share!
We've set up a new email list especially for sharing these kinds of
ideas:

mobile-ideas@lists.rackspace.com

If you have an idea, please share it!  Sure, someone may have already
thought of it, and maybe it's not something we can do right awayŠ but
then
again, maybe it's BRILLIANT and GAME CHANGING!  So get typing!   We
look
forward to hearing all the great ideas Rackers come up with!

---
Greg Herlein
Director, Software and Product Development
Rackspace Hosting
415-368-7546
@gherlein





