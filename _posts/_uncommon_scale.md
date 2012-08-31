---
layout: post.html
title: Cloud Scaling Anti-patterns or Painless Scaling, scale early, scale often
summary: Scaling your web app or service is a nice problem to have.  When, the runway has some potholes you will want to avoid.
---

[specific examples]
[illustartions - asciiflow, pen and paper]


[day of your repentance quote.]

Scaling your app or service is often described by startup veterans as "a nice problem to have," something that "you should worry about later, when&mdash;or if&mdash;your app takes off". People love to hear scaling war stories; how suddenly an app goes viral at 3am Sunday morning, and the team has just hours to rewrite and swap out half their backend, else face ironic destruction at the hands of their fans.

Stories about painless scaling and team members being home in time for dinner are far less common. Such experiences simply aren't sensational enough to gain much attention. That's a real shame, because sleepless nights and Rockstar-fueled hackathons should not be promoted as *business as usual*, but *the worst possible outcome*. 

Eventually, we software developers will discover elegant solutions to the problem of scaling cloud apps, making knee-jerk, duct-tape engineering obsolete. In the meantime, I'm convinced we can avoid a lot of the pain and suffering by investing more time up-front in thinking about architecture, carefully choosing a hosting provider, and making continuous integration and deployment a non-negotiable part of our process.

# Know Thy Limits

[quote, scriptural or classic, poor in spirit, inherit the earth]

Architectural self-awareness pays big dividends, particularly when applied at the beginning of a project. What tradeoffs are you making, and why? How far will your initial design take you? What will you do if usage spikes? The point is this: spending a little time up front thinking ahead, pushing and prodding early iterations of your app until they break&mdash;then picking up the pieces and putting them back together&mdash;will help you avoid a lot of nasty suprises later on in.

Now, you don't need to create a massively scalable system right out of the gate; you can't afford to. On the other hand, you need only barter a few days' work to become reasonably familiar with the limitations&mdash;in terms of scalability, reliability and efficiency&mdash;inherent in the various components of your toolbox, including programming languages, frameworks, operating system, database, etc.

Truth. This is your goal in the first week of your new project. Don't simply choose the first design, the first platform, or the first algorithm that comes to mind. Challenge yourself to think of something better. Experiment. It takes time to discover the best tools for the job and the best way to apply those tools.

  * **Prototype your ideas.** Bring them into the real world. Iterating on a protoype is virtually free. Build one to throw away. 
  * **Conduct fire drills.** Break your software before your users do. Watermark your system's performance and reliability, and take a few minutes to consider (a) what simple adjustments you might make to raise that watermark, and (b) how you can design your system to make it as easy as possible to add capacity on the fly without having to swap out half the components in the heat of battle.
  * **Monitor early, often.** These days, there are plenty of ways to quickly add monitoring to your daemons and databases. It doesn't take long to whip up a simple dashboard containing a few graphs and statistics. Monitoring  you anticipate scaling problems, so you can fix them while the rest of the world is awake&mdash;sans 48-hour hackathons and a sleeping bag under the desk.

You can't anticipate everything about how your cloud service or app will need to scale to meet demand. What you *can* do, however, is create a flexible architecture and educate yourself, such that you can rapidly diagnose system crashes and move quickly to resolve the root cause.

  * **Prototype your ideas.** Bring them into the real world. Iterating on a protoype is virtually free compared to trying to do the same thing once your ship is in the water. Build one to throw away. No amount of googling can substitute for first-hand experience. 
  * **Conduct fire drills.** Break your software before your users do. Watermark your system's performance and reliability, and take a few minutes to consider (a) what simple adjustments you might make to raise that watermark, and (b) how you can design your system to make it as easy as possible to add capacity on the fly without having to swap out half the components in the heat of battle.
  * **Bake monitoring into your service from the beginning.** These days, there are plenty of ways to quickly add monitoring to your daemons and databases. It doesn't take long to whip up a simple dashboard containing a few graphs and statistics. Such a dashboard helps you anticipate scaling problems before they turn into a crisis, and helps you gauge your success when you deploy optimizations. 

# Demand Awesome Hosting

Datacenter migrations are the last thing you want to worry about in the middle of a scaling crisis. When evaluating hosting providers, choose a good home for your app. The ideal hosting provider not only has expertise in your platform of choice, but also offers services which scale from a single virtual machine in one DC, to 100's of boxes spread across multiple regions.

While it is *possible* to run highly-trafficked cloud services on Amazon's EC2 instances or Rackspace's Cloud Servers, bare metal might be just the thing to solve your scaling problems in a cost-effective way. 37signals takes this approach with their DB boxes. It frees them to scale Basecamp and other popular apps *up*, as well as *out*. Need more RAM? A faster disk? 10g nic? Hardware TLS termination? No problem. 

I prefer hosting companies that offer hybrid cloud solutions, so I have the option to provision dedicated boxes and appliances as needed. The I/O tax and cost structure for large VMs are serious tradeoffs that I'd rather not be locked into.

If you find yourself implementing silly and outrageous workarounds for deficiencies in your hosting platform, your cloud provider isn't doing their job. You should demand reliability and solid performance for your money. IaaS should not only abstract away hardware, but also hardware failures&mdash;so you don't have to worry about it. 

Elasticity is only part of a great cloud solution. Choose a cloud provider that understands this. There are several good choices out there.

# Trust Your Code

Security (more on this in a different post)
Deploy Changes in Minutes
Ensure Quality
Early feedback on problems
Start with basic set of tests, add more as you go
Include security testing
Code style (readable, pinpoint problems quickly)
Peer review
