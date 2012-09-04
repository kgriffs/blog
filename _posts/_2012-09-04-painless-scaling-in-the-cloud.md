---
layout: post.html
title: Painless Scaling in the Cloud
summary: Scaling your web app or service is a nice problem to have, but just because you may never need to do it doesn't mean you shouldn't plan for it.
---

[specific examples, tools]
[illustartions - asciiflow, pen and paper]
[consolodate voice - us/you/i/we]

Scaling your app or service is often described by startup veterans as "a nice problem to have," something that "you should worry about later, when&mdash;or if&mdash;your app takes off". People love to hear war stories re scaling; how suddenly an app goes viral at 3 am Sunday morning, and the team has just hours to rewrite and swap out half their backend before their world comes to a rather unfortunate end.

Stories about painless scaling and team members being home in time for dinner are far less common. Such experiences simply aren't sensational enough to gain much attention. That's a real shame. Sleepless nights and Rockstar-fueled hackathons **should not be the norm**, but the exception.

Eventually, we software developers will discover elegant solutions to the problem of scaling cloud apps, making knee-jerk, duct-tape engineering obsolete. In the meantime, I'm convinced we can avoid a lot of pain by investing a little more time up-front in prototyping ideas, carefully choosing a hosting provider, and putting continuous integration and deployment at the heart of everything we do.

# Know Your Limits

[quote, scriptural or classic, poor in spirit, inherit the earth]

Architectural self-awareness pays big dividends. What tradeoffs are you making, and why? How far will your initial design take you? What will you do if usage spikes? Pushing and prodding early iterations of your app until they break&mdash;then picking up the pieces and putting them back together&mdash;will help you avoid a lot of nasty suprises later on in. At the very least, you will know what you are getting yourself into.

You don't need to create a massively scalable system right out of the gate; even if you wanted to, you probably can't afford to. On the other hand, you need only barter a few days' work to become reasonably familiar with the limitations&mdash;in terms of scalability, reliability and efficiency&mdash;inherent in the various components of your toolbox. How well do you grok your programming language, framework, OS, DB, etc.?

Experiment. Don't simply choose the first design, the first platform, or the first algorithm that comes to mind. **Challenge yourself to think of something better.** Some things I do to test ideas early and often:

  1. **Prototype ideas.** Bring them into the real world. Make ideas stand up and dance to reveal their true nature. Speculation is dangerous; avoid it.
  1. **Conduct fire drills.** Break software before users do. Watermark system performance and reliability, and take a few minutes to consider (a) what simple adjustments can be made to raise that watermark, and (b) whether a given architecture affords adding capacity, without having to rearchitect major components.
  1. **Monitor early, often.** Monitoring helps you anticipate scaling problems so that you can fix them during regular hours. These days, there are plenty of ways to quickly add monitoring to your daemons and databases. It doesn't take long to whip up a simple dashboard containing a few graphs and statistics. Set up a few alerts so everyone knows when boxes are running hot, when connections are dropped, and when deamons crash.

Certainly, you can't anticipate everything. It is a waste of time to even try. What you *can* do is create a flexible architecture and anticipate your system's limitations. By doing these two things, you equip yourself to more effectively overcome scaling challenges, giving yourself a better chance at making it home in time for dinner.

# Choose a Scalable Hosting Platform

Datacenter migrations are the last thing you want on your mind in the middle of a scaling crisis. When evaluating hosting providers, choose a good home for your app. The ideal hosting provider not only has expertise in your tech stack, but also offers services which scale from a single virtual machine in one DC, to 1000's of boxes hosted around the world.

If you find yourself implementing silly and outrageous workarounds for deficiencies in your hosting platform, your cloud provider isn't doing their job. You should demand reliability and solid performance for your money. IaaS is not only an abstraction of physical hardware, but also an abstraction of physical durability. The less these abstractions leak, the better.

For some parts of your system, running on cloud IaaS is the wrong approach. are more trouble than they are worth. While it *is* possible to run highly-trafficked cloud services on Amazon's EC2 instances or Rackspace's Cloud Servers, a bare-metal server can be a less painful&mdash;and less costly&mdash;way to scale parts of your system. 37signals runs their DB cluster on custom boxes. This approach frees them to scale Basecamp and other popular apps *up*, as well as *out*. Need more RAM? A faster disk? How about a 10g nic? No problem.

Personally, I prefer hosting companies that offer hybrid solutions, so that I can provision dedicated boxes and appliances that interoperate with my cloud servers. The I/O tax and cost structure for large VMs does not suit every use case (e.g., hosting an RDBMS).

Generally speaking, if you spend a little more time up front researching the best **long-term** host for your project, you will save yourself a significant amount of grief.

# Trust Your Code

Continuous integration and delivery (CI) should be at the heart of every cloud software development process. CI engenders trust in your code base, allowing you and your team to quickly roll out new features and optimizations. Not only does this ability help you outpace the competition, but also empowers your team to act quickly in an emergency.

The best CI pipelines:

  1. **Make peer code reviews** the first line of defense. Code reviews are suprisingly effective at catching bugs and suboptimal designs when they are the cheapest to fix.
  1. **Include multiple environments**, such as *dev*, *test*, *staging* and *production*. The *staging* environment mirrors *production* as close as possible, making *staging* ideal for smoke-testing, watermarking, and benchmarking. The *test* environment provides a reasonably stable deployment suitable for integration testing, while *dev* is an inherently unstable environment used to prove freshly-minted code.
  1. **Run stages in parallel**. Build 42 can be running in *dev* while build 41 is in *test*, and build 40 is in *staging* being vetted for final deployment to *production*, which is running build 39.
  1. **Order simple, fast tests** before complex, slow ones. I.e., there's no sense in running expensive tests when the code doesn't even compile.
  1. **Include unit, integration, and security tests.** Break your own software, rather than forcing users to do it for you. Quality is *your* job, not theirs.
  1. **Run static analysis tools.** Even the most skilled programmers in the world still make stupid mistakes. There's an app for that.
  1. **Enforce a consistent coding style.** Developers spend a lot more time reading code than writing it. Make your code easy to grok, and you will thank yourself later.

You don't need to invest a lot of time setting up your CI pipeline. Start small with only a few automated tests and two environments; one for development, and one for production. Then, take a few hours each week to tweak and improve your process until you are no longer nervous about shipping code every day.

# Q.E.D.

By spending a little more time planning ahead, and by putting in place a trustworthy continuous integration and deployment pipeline, you will avoid a lot of sleepless nights and shattered relationships when your app blows up. And I sincerely hope it does.

After all, that is a nice problem to have.

@kgriffs
