When deploying a web head,

https://gist.github.com/kgriffs/4027835

## Security Tweaks

If you've never had a server that's been attacked, you've never had a
server. Here are two simply security tweaks you can make to the kernel
to help combat the bad guys. {footnote @ comprehensive security plan}

### net.ipv4.tcp_syncookies

Enabling this option mitigates SYN flood attacks. [what is a SYN flood? How does
this setting help?]

```conf
net.ipv4.tcp_syncookies = 1
```

### net.ipv4.conf.all.log_martians

This setting logs mischieveous packets to help you detect certain types of
attacks.

[what is an evil packet vs. a martian?]
[how do attackers leverage evil packets?]
[what log?]
[setting up alerting]

```conf
net.ipv4.conf.all.log_martians = 1
```

## Throughput Tweaks

blah

## Concurrency Tweaks
blah

--


lots of data

security
high throughput
high concurrency


profiles

web head
load generator




p.s - want to use these on load generator (call out subset)