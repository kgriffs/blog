---
layout: post.html
title: Painless Scaling in the Cloud
summary: Scaling your web app or service is a nice problem to have, but just because you may never need to do it doesn't mean you shouldn't plan for it.
---

[specific examples, tools]
[illustartions - asciiflow, pen and paper]
[consolodate voice - us/you/i/we]
[conclusion]
[paragraphs, style book]

[day of your repentance quote.]

Scaling your app or service is often described by startup veterans as "a nice problem to have," something that "you should worry about later, when&mdash;or if&mdash;your app takes off". People love to hear scaling war stories; how suddenly an app goes viral at 3 am Sunday morning, and the team has just hours to rewrite and swap out half their backend, else face ironic destruction at the hands of their fans.

Stories about painless scaling and team members being home in time for dinner are far less common. Such experiences simply aren't sensational enough to gain much attention. That's a real shame, because sleepless nights and Rockstar-fueled hackathons should not be promoted as *business as usual*, but *the worst possible outcome*. 

Eventually, we software developers will discover elegant solutions to the problem of scaling cloud apps, making knee-jerk, duct-tape engineering obsolete. In the meantime, I'm convinced we can avoid a lot of the pain and suffering by investing more time up-front in thinking about architecture, carefully choosing a hosting provider, and making continuous integration and deployment a non-negotiable part of our process.

# Know Your Limits

[quote, scriptural or classic, poor in spirit, inherit the earth]

Architectural self-awareness pays big dividends, particularly when applied at the beginning of a project. What tradeoffs are you making, and why? How far will your initial design take you? What will you do if usage spikes? The point is this: spending a little time up front thinking ahead, pushing and prodding early iterations of your app until they break&mdash;then picking up the pieces and putting them back together&mdash;will help you avoid a lot of nasty suprises later on in.

You don't need to create a massively scalable system right out of the gate; even if you wanted to, you probably can't afford to. On the other hand, you need only barter a few days' work to become reasonably familiar with the limitations&mdash;in terms of scalability, reliability and efficiency&mdash;inherent in the various components of your toolbox, including programming languages, frameworks, operating system, database, etc.

Don't simply choose the first design, the first platform, or the first algorithm that comes to mind. Challenge yourself to think of something better. Experiment. It takes time to discover the best tools for the job and the best way to apply those tools. A few suggestions on how to do this:

  1. **Prototype ideas.** Bring them into the real world. Make your ideas stand up and dance so you can review their form. Speculation is dangerous; avoid it.
  1. **Conduct fire drills.** Break your software before your users do. Watermark your system's performance and reliability, and take a few minutes to consider (a) what simple adjustments you might make to raise that watermark, and (b) how you can design your system to make it as easy as possible to add capacity on the fly without having to swap out half the components in the heat of battle.
  1. **Monitor early, often.** These days, there are plenty of ways to quickly add monitoring to your daemons and databases. It doesn't take long to whip up a simple dashboard containing a few graphs and statistics. Monitoring  you anticipate scaling problems, so you can fix them while the rest of the world is awake&mdash;sans 48-hour hackathons and a sleeping bag under the desk.

You can't anticipate everything about how your cloud service or app will need to scale to meet demand. What you *can* do, however, is create a flexible architecture and educate yourself, such that you can rapidly diagnose system crashes and move quickly to resolve the root cause.

# Choose a Scalable Hosting Platform

Datacenter migrations are the last thing you want to worry about in the middle of a scaling crisis. When evaluating hosting providers, choose a good home for your app. The ideal hosting provider not only has expertise in your platform of choice, but also offers services which scale from a single virtual machine in one DC, to 100's of boxes spread across multiple regions.

While it *is* possible to run highly-trafficked cloud services on Amazon's EC2 instances or Rackspace's Cloud Servers, a bare-metal server can be a more straighforward, cost-effective way to scale parts of your system. 37signals takes this approach with their DB boxes. It frees them to scale Basecamp and other popular apps *up*, as well as *out*. Need more RAM? A faster disk? How about a 10g nic? No problem. 

I prefer hosting companies that offer hybrid cloud solutions, so I have the option to provision dedicated boxes and appliances as needed. The I/O tax and cost structure for large VMs are serious tradeoffs that I'd rather not be locked into.

If you find yourself implementing silly and outrageous workarounds for deficiencies in your hosting platform, your cloud provider isn't doing their job. You should demand reliability and solid performance for your money. IaaS should not only abstract away hardware, but also hardware failures&mdash;so you don't have to worry about it. 

Elasticity is only part of a great cloud solution. Choose a cloud provider that understands this. There are several good choices out there. Spend some time up front researching the best host for *your* project, and you won't be sorry.

# Trust Your Code

Continuous integration and delivery (CI/CD) should be at the heart of every cloud software development process. CI/CD engenders trust in your code base, allowing you and your team to quickly roll out new features and optimizations. Not only does this ability help you outpace the competition, but also empowers your team to act quickly in an emergency.

The best CI/CD pipelines:

  1. Make **peer code reviews the first stage.** Code reviews are suprisingly effective at catching bugs and suboptimal designs when they are the cheapest to fix. 
  1. Include **multiple environments**, such as *dev*, *test*, *staging* and *production*. Staging mirrors production as close as possible and is used for smoke-testing, watermarking, and benchmarking. *Test* provides a reasonably stable environment for running integration tests, while *dev* is a scratch pad where you experiment and are free to break things on purpose (or accident).
  1. Run stages **in parallel**. Build 42 can be running in *dev* while build 41 is in *test*, and build 40 is in *staging* being vetted for final deployment to *production*.
  1. Order **simple, fast tests** before complex, slow ones. I.e., there's no sense in running expensive tests when the code doesn't even compile.
  1. Include **unit, integration, and security tests.** Break your own software, rather than forcing users to do it for you. Quality is *your* job, not theirs.
  1. Run **static analysis tools.** Even the most skilled programmers in the world still make stupid mistakes on occasion.
  1. Enforce a **consistent coding style.** Developers spend a lot more time reading code than writing it. Make your code as easy to grok as possible, and I guarantee you will thank yourself later.

You don't need to invest a lot of time setting up your delivery pipeline. The most important thing is that you have one. Start small with only a few automated tests and two environments; one for development, and one for production. Then, take a few hours each week to tweak and improve your delivery process until it is ready for prime time.

# Q.E.D.

By spending a little more time planning ahead and putting in place a rock-solid delivery process, you will avoid a significant amount of pain down the road if your project takes off, which I sincerely hope it does. Otherwise, what's the point of building it in the first place? 

Happy hacking.

@kgriffs
