---
layout: post.html
title: Painless Scaling in the Cloud
summary: Scaling your web app or service is a nice problem to have, but just because you may never need to do it, doesn't mean you shouldn't plan for it.
tags: [Essays]
id: 66447D28-EDFC-11E1-A556-6E52F4FE7012
---

Scaling your app or service is often described by startup veterans as "a nice problem to have," something that "you should worry about later, if/when your app takes off". People love to hear epic war stories about just-in-time scaling; how suddenly widg.it went viral at 3 am on a Sunday morning, and the team only had a few hours to rewrite half their system, switch data centers, and shard their database to stop it from crashing every ten minutes.

<img src="/assets/images/cloud-scaling-talk.png" alt="Cloud Scaling Talk" />

Stories like this can fool you into thinking there's no other way to get to web-scale. That's just plain silly. With a little less procrastination, and a little more foresight, you can enjoy a relatively painless experience scaling your cloud app or service.

(Mostly) painless scaling is possible; I've experienced it first-hand. Sadly, such experiences simply aren't sensational enough to make the front page of Hacker News. That's a real shame. Sleepless nights and Rockstar-fueled hackathons **should not be the norm**, but the exception. 

Survival by accident isn't something we should be proud of. 

> The general who wins a battle makes many calculations in his temple ere the battle is fought. The general who loses a battle makes but few calculations beforehand. Thus do many calculations lead to victory, and few calculations to defeat: how much more no calculation at all! It is by attention to this point that I can foresee who is likely to win or lose.

> ~ Sun Tzu 

Eventually, we software developers will discover elegant solutions to the problem of scaling cloud apps, making knee-jerk, duct-tape engineering obsolete. In the meantime, we can avoid a lot of pain by investing more time up-front in proving ideas, carefully choosing a hosting provider, and putting continuous integration and deployment at the heart of everything we do.

# Web-scale Architecture: Build one to Throw Away

> If you know the enemy and know yourself, you need not fear the result of a hundred battles If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle.

> ~ Sun Tzu 

Architectural awesomeness requires patience, humility and experimentation. What trade-offs are you making, and why? How far will your initial design take you? What will you do if usage spikes? Pushing and prodding early iterations of your app until they break&mdash;then picking up the pieces and putting them back together again&mdash;will help you avoid a lot of nasty surprises. At the very least, you will know what you are getting yourself into.

<img class="left" src="/assets/images/poor-cloud-ideas.png" alt="Poor Cloud Ideas (Thrown Away)" />

You don't need to create a massively scalable system right out of the gate; even if you wanted to, you probably can't afford it. On the other hand, you need only barter a few days' work to become reasonably familiar with the limitations&mdash;in terms of scalability, reliability and efficiency&mdash;inherent in the various components of your toolbox. How well do you grok your programming language, web framework, operating system, or database server?

Experiment. Don't simply choose the first design, the first platform, or the first algorithm that comes to mind. **Challenge yourself to think of something better.** Some things I do to test ideas early and often:

  1. **Prototype ideas.** Bring them into the real world. Make ideas stand up and dance to reveal their true nature. Second-hand anecdotes are inferior to taking something for a test drive yourself. Speculation is dangerous; avoid it. 
  1. **Conduct fire drills.** Break software before users do. Watermark system performance and reliability, and take a few minutes to consider (a) what simple adjustments can be made to raise that watermark, and (b) whether your design affords scaling, without having to re-architect major components.
  1. **Monitor early, often.** Monitoring helps you anticipate scaling problems so that you can fix them while the sun's still shining. These days, there are [plenty][statsd] of [ways][cloud-monitoring] to quickly add [monitoring][cloud-watch] to your servers, daemons and databases. It doesn't take long to whip up a simple [dashboard][graphite] containing a few graphs and statistics. Set up a few alerts so everyone knows when boxes are running hot, when connections are dropped, and when daemons crash.

[statsd]: https://github.com/etsy/statsd
[cloud-monitoring]: http://www.rackspace.com/cloud/public/monitoring/
[cloud-watch]: http://aws.amazon.com/cloudwatch/
[graphite]: http://graphite.wikidot.com/


Certainly, you can't anticipate everything. Trying is a waste of time. What you *can* do is create a flexible architecture and anticipate your system's limitations. By doing these two things, you equip yourself to more effectively overcome scaling challenges, giving yourself a better chance at making it home in time for dinner at the end of the day.

# Cloud Hosting: An Intimate Relationship

> We cannot enter into alliances until we are acquainted with the designs of our neighbors.

> ~ Sun Tzu

Data center migrations are the last thing you want on your mind in the middle of a scaling crisis. When evaluating hosting providers, choose a good home for your app. The ideal hosting provider not only has expertise in your tech stack, but also offers services which scale from a single virtual machine in one DC, to 1000 boxes hosted around the world.

If you find yourself implementing silly and outrageous workarounds for deficiencies in your hosting platform, your cloud provider is doing it wrong. You should demand reliability and solid performance for your money. IaaS is not only an abstraction of physical hardware, but also an abstraction of physical durability. The less these abstractions leak, the better.

<img src="/assets/images/cloud-borg.png" alt="Hybrid Cloud Hosting, ala The Borg" />

For some parts of your system, running on a virtualized platform is the wrong approach. While it's certainly *possible* to run highly-trafficked cloud services on Amazon's EC2 instances or Rackspace's Cloud Servers, **it isn't always wise**. A bare-metal server can be a less painful&mdash;and less costly&mdash;way to scale parts of your system. For example, 37signals runs their DB cluster on custom boxes. This approach frees them to scale Basecamp and other popular apps geometrically (*up*, as well as *out*). Need more RAM? A faster disk? How about a 10g nic? No problem.

Personally, I prefer hosting companies that offer hybrid solutions, so that I can provision dedicated boxes and appliances that inter-operate with my cloud servers. I don't need to do this out of the gate; cloud servers will do the job. But there will come a time when that's no longer the case. The I/O tax and cost structure for virtual machines doesn't work out well when scaling certain components beyond a certain point (e.g., an RDBMS).

Generally speaking, if you spend a little more time up front researching the best **long-term** host for your project, you will save yourself a significant amount of grief when it comes time to scale your system.

# Continuous Integration: Trust Your Code

> Thus it is that in war the victorious strategist only seeks battle after the victory has been won, whereas he who is destined for defeat, first fights, and afterwards looks for victory.

> ~ Sun Tzu

Continuous integration and delivery (CI) belongs at the heart of cloud software development&mdash;even for small, two-person startups. CI engenders trust in your code base, allowing you and your team to quickly roll out new features and optimizations. This ability is an absolute lifesaver during emergencies.

<img class="center" src="/assets/images/cloud-continuous-integration.png" alt="Hybrid Cloud Hosting, ala The Borg" />

A good CI system will break your code before the customer does. This is what you want. The earlier in your development process that you find and fix problems, the cheaper (and less embarrassing) it is to take care of those problems.

Some tips for making your CI awesome:

  1. **Employ peer code reviews** as the first line of defense. Code reviews are surprisingly effective at catching bugs and suboptimal designs when they are the cheapest to fix.
  1. **Run unit, integration, and security tests.** Break your own software, rather than forcing users to do it for you. Quality is *your* job, not theirs.
  1. **Run static analysis tools.** Even the most skilled programmers in the world still make stupid mistakes. There's an app for that.
  1. **Run simple, fast tests** before complex, slow ones. E.g., there's no sense in running expensive tests when the code doesn't even compile.
  1. **Enforce a consistent coding style.** Developers spend a lot more time reading code than writing it. Make your code easy to grok, and you will thank yourself later.
  1. **Include multiple environments**, such as *dev*, *test*, *staging* and *production*. The *staging* environment mirrors *production* as close as possible, making *staging* ideal for smoke-testing, watermarking, and benchmarking. The *test* environment provides a reasonably stable deployment suitable for integration testing, while *dev* is an inherently unstable environment used to prove freshly-minted code.
  1. **Pipeline stages**. Build 5142 can be running in *dev* while build 5141 is in *test*. At the same time, build 5140 can be in *staging*, where it is vetted before deployment to *production*. This approach requires more build servers, but delivers feedback earlier and more often.

You don't need to invest a lot of time and money setting up your CI pipeline. Start small with only a few automated tests and two environments; one for development, and one for production. Use a free CI system such as BuildBot, CruseControl.NET, or Jenkins. Then, take a few hours each week to tweak and improve your process until you are no longer nervous about shipping code on the same day it's written.

# Q.E.D.

By spending a little more time planning ahead, and by putting in place a trustworthy continuous integration and deployment pipeline, you have a good chance at avoiding sleepless nights and shattered relationships when your app blows up&mdash;and I sincerely hope it does.

After all, that's a nice problem to have.

@kgriffs
