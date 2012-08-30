---
layout: post.html
title: Cloud Scaling Anti-patterns or Painless Scaling, scale early, scale often
summary: Scaling your web app or service is a nice problem to have.  When, the runway has some potholes you will want to avoid.
---

day of your repentance quote.

Scaling your app or service is often described by startup veterans as "a nice problem to have," something that "you should worry about later, when&mdash;or if&mdash;your app takes off". People love to hear scaling war stories; how suddenly an app goes viral at 3am Sunday morning, and the team has just hours to rewrite and swap out half their backend, else face ironic destruction at the hands of their fans.

Stories about painless scaling and team members being home in time for dinner are far less common. Such experiences simply aren't sensational enough to gain much attention. That's a real shame, because sleepless nights and Rockstar-fueled hackathons should not be promoted as *business as usual*, but *the worst possible outcome*. 

Eventually, we software developers will discover elegant solutions to the problem of scaling cloud apps, making knee-jerk, duct-tape engineering obsolete. In the meantime, I'm convinced we can avoid a lot of the pain and suffering by investing more time up-front in thinking about architecture, carefully choosing a hosting provider, and making continuous integration and deployment a non-negotiable part of our process.

[Create illustrations for each majore point below]

# Know Thy Limits

[quote, scriptural or classic, poor in spirit, inherit the earth]

Architectural self-awareness pays big dividends, particularly when applied at the beginning of a project. What tradeoffs are you making, and why? How far will your initial design take you? What will you do if usage spikes? The point is this: spending a little time up front thinking ahead, pushing and prodding early iterations of your app until they break&mdash;then picking up the pieces and putting them back together&mdash;will help you avoid a lot of nasty suprises later on in.

Now, you don't need to create a massively scalable system right out of the gate; you can't afford to. On the other hand, you need only barter a few days' work to become reasonably familiar with the limitations&mdash;in terms of scalability, reliability and efficiency&mdash;inherent in the various components of your toolbox, including programming languages, frameworks, operating system, database, etc.

Truth. This is your goal in the first week of your new project. Don't simply choose the first design, the first platform, or the first algorithm that comes to mind. Challenge yourself to think of something better. Experiment. It takes time to discover the best tools for the job and the best way to apply those tools.

Useful excercises:

  * **Prototype your ideas.** Bring them into the real world. Iterating on a protoype is virtually free compared to trying to do the same thing once your ship is in the water.Build one to throw away. No amount of googling can substitute for first-hand experience. 
  * **Conduct fire drills.** Break your software before your users do. Watermark your system's performance and reliability, and take a few minutes to consider (a) what simple adjustments you might make to raise that watermark, and (b) how you can design your system to make it as easy as possible to add capacity on the fly without having to swap out half the components in the heat of battle.
  * **Bake monitoring into your service from the beginning.** These days, there are plenty of ways to quickly add monitoring to your daemons and databases. It doesn't take long to whip up a simple dashboard containing a few graphs and statistics. Such a dashboard helps you anticipate scaling problems before they turn into a crisis, and helps you gauge your success when you deploy optimizations. 

You can't anticipate everything about how your cloud service or app will need to scale to meet demand. What you *can* do, however, is create a flexible architecture and educate yourself, such that you can rapidly diagnose system crashes and move quickly to resolve the root cause.

-----------------

3 versions of note
plan up front
excercise before opening store

* Fire Drills
* Watermarking
* Prototyping
* Monitoring - New Relic, logs, MaaS, alerts, dashboard

# Avoid Painful Datacenter Migrations

* inexpensive, scale up
* hybrid, efficient, more cost-effective
* support

# Trust Your Code

Security (more on this in a different post)
Deploy Changes in Minutes
Ensure Quality
Early feedback on problems
Start with basic set of tests, add more as you go
Include security testing
Code style (readable, pinpoint problems quickly)
Peer review


suggested tools for each category



 use several strategies to get the job done with considerably fewer trips to Home Depot.

 a lot less fun when that's *you* passed out under your desk.

This advice to is so common, it is often taken as 

ones that make it, less painful, don't make for a good story



However, you can avoid the inevitable sleepless nights and Rockstar-fueled hackathons 


by spending some quality time with a pencil and paper spending a little bit more time up-front thinking through your design and prototyping your ideas.

Duct-tape engineering is quite common in the world of connected applications.

Eventually, we will discover elegant solutions to the problem of scaling cloud apps, making duct-tape engineering obsolete. In the meantime, you can use several strategies to get the job done with considerably fewer trips to Home Depot. 

Strategy: Do not procrastinate the day of your repentance

simulated repentance, fire drills
analytics early, often, plus monitoring

Strategy: All hosts are not created equal, cloud !== scale

trial run

Strategy: CI/CD




pencil and paper

Strategy: CI/CD

Strategy: Reinvent the Wheel

Strategy: Design for Efficiency

Strategy: Analytics Early, Often (DevOps, monitoring dashboards) 

Strategy: Choose your Hosting Wisely

do up front, when not stressed, pick long-term, hybrid. Address cost. Some hosts are extremely inefficient and cost a ton at scale.

cloud != scale

Strategy: Watermarking

Strategy: Design for Scaling Out

Strategy: Reduce Hops

Less to manage, more efficient, performant - balance with separation of concerns.



These strategies all follow theme. Looks for more...

duct-tape airplane 

If I build an airplane... crazy, right? - stories of airplanes early days, chicken wire and duct-tape. 


The code goes, but if it works, who cares?

Is it possible to avoid rewriting half your system in-flight?   

 

  decisions have a way of coming back from the dead again and again. [Talk about three ways to make scaling less painful if you are lucky enough to have such a nice problem.]

 if you make it big. Here are a few

# 3 - 5 points

* Don't Reinvent the Wheel
* Scale out, not up
* Cloud Hosting === Scalable
* Can't anticipate
  * hosting provider can scale with you, metrics, testing, fire drill
  * my app never crash
* Too costly

# Summary


having to work for three days straight to swap out half your system when and then pass out under your desk to swap out half your system when suddenly that 'nice problem' falls into your lap

Startups that follow this advice and survice to make it big like to tell war stories, based on their experiences having to scale their systems at a moment's notice. While

explaining how, for example, everything went to heck at 3am one Thursday morning, and they had less than 1 hour to swap out half their system or die. Such

While such stories are fun to hear and make for a good tech talk, certainly entertaining, and virtually guarantee a spot on Hacker News, are experiences like these an inevitable consequence of success?

Twitter
Instagram
DDG
Facebook
Jungle Disk

choose the right tool for the job (twitter, facebook)

cost, scaling is expensive, planning for scalability from the beginning is expensive, requires too much expertise.


don't reinvent the wheel

out, not up? maybe.

HTTP is too slow

we can do devops later

we can clean up this code later

early testing, benchmarking, we have no idea what real usage is like

my app will never crash

I can always scale up

don't worry about provider

The Cloud(tm) will not save you -- this hot new tech will save us - when your app goes viral, noone can save you. Noone has had this specific problem before.

iterate, but be flexible, etc.

Fallacy: embrace technical debt... VC mindset? Much riskier... At mininum, much more painful.

specific examples

adjectives

illustrations
