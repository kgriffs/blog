When deploying a web head,

https://wiki.archlinux.org/index.php/Sysctl#TCP.2FIP_stack_hardening

https://gist.github.com/kgriffs/4027835
http://www.webhostingtalk.com/showthread.php?t=257654
http://www.nateware.com/linux-network-tuning-for-2013.html

http://support.atmail.com/display/DOCS/Tuning+Sysctl+Paramaters+For+Heavily+Loaded+Systems
http://dak1n1.com/blog/12-nginx-performance-tuning

https://www.frozentux.net/ipsysctl-tutorial/chunkyhtml/theconfvariables.html

clarify that this is for Linux

[link to man page]

## Security Tweaks

If you've never had a server that's been attacked, you've never had a server. Here are two simply security tweaks you can make to the kernel to help combat the bad guys. {footnote @ comprehensive security plan}

### Enable SYN Cookies

A [SYN flood](https://en.wikipedia.org/wiki/SYN_flood) is a DoS attack that works by sending a bunch of TCP connection requests (SYN) but ommitting the followup (ACK) required to finalize the connection. This eats up server resources by creating an increasingly large number of half-negotiated connections, until no new connections can be established.

Using SYN cookies is one strategy for mitigating SYN floods. A SYN cookie allows a server to discard SYN queue entries when the queue fills up, and reconstruct them later for legitimate clients that subsequently submit an ACK for the purged SYN. In this way, bogus SYNs can be discarded without blocking legitimate connection attempts.

Enable SYN cookies in the network stack using this option in *sysctl.conf*:

```conf
net.ipv4.tcp_syncookies = 1
```

### Log Evil Packets

Occasionaly your server will receive a network packet containing a so-called "impossible" address. An impossible address is one that is not reachable from the server's network interface.

This setting logs suspicious packets to help you detect certain types of attacks that rely on spoofing addresses.

[what is an evil packet vs. a martian?]
[how do attackers leverage evil packets?]
[what log?]
[setting up alerting]

```conf
net.ipv4.conf.all.log_martians = 1
```

## Tweak how the flow of kernel messages is throttled.

Certain kinds of kernel warning messages are rate-limited. This helps avoid clogging up your log (i.e., /var/log/messages), but sometimes the default settings make it hard to diagnose a scaling problem, or even an attack on your box. If you are seeing lots of lines in your log about messages being suppressed, and it isn't clear what the initial message was, you can try increasing the burst limit or decreasing the rate limit:

```conf
# How many messages to allow through before throttling
kernel.printk_ratelimit_burst = 10

# Minimum number of seconds to wait between logging each message (default 5 seconds)
kernel.printk_ratelimit = 5
```

## Latency Tweaks


## Throughput Tweaks


## Concurrency Tweaks

Web servers typically have to serve a large number of concurrent requests. The request rate hitting your server will grow and shrink constantly, and sometimes you'll have to handle some extraordinary bursts. To avoid simply dropping requests whenever the load on your server spikes and your website or app can't keep up, there are a few things you can do.

First of all, you can increase the number of connection requests the server will queue before starting to drop subsequent connection attempts. The default is 128, which is far too low for a busy web server. You will want to increase the queue length to at least 1024, and you may go up to 50000 or even higher.

What you choose for this setting will depend on the size of the traffic bursts you are seeing in production, and how quickly each burst can be resolved. The higher and wider the bursts, the longer the queue needs to be, to avoid dropping connection requests. You'll have to experiment to find the right setting for your particular server capacity and workload.


```conf
net.core.somaxconn = 50000
```

--


lots of data

security
high throughput
high concurrency


profiles

web head
load generator

p.s - which ones to use these on load generator (call out subset)



# Discourage Linux from swapping idle server processes to disk (default = 60)
vm.swappiness = 10


# --------------------------------------------------------------------
# The following allow the server to handle lots of connection requests
# --------------------------------------------------------------------

# Increase number of incoming connections that can queue up
# before dropping
net.core.somaxconn = 50000

# Handle SYN floods and large numbers of valid HTTPS connections
net.ipv4.tcp_max_syn_backlog = 30000

# Increase the length of the network device input queue
net.core.netdev_max_backlog = 5000

# Increase system file descriptor limit so we will (probably)
# never run out under lots of concurrent requests.
# (Per-process limit is set in /etc/security/limits.conf)
fs.file-max = 100000

# Widen the port range used for outgoing connections
net.ipv4.ip_local_port_range = 10000 65000

# If your servers talk UDP, also up these limits
net.ipv4.udp_rmem_min = 8192
net.ipv4.udp_wmem_min = 8192

# --------------------------------------------------------------------
# The following help the server efficiently pipe large amounts of data
# --------------------------------------------------------------------

# Disable source routing and redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.accept_source_route = 0

# Disable packet forwarding.
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Disable TCP slow start on idle connections
net.ipv4.tcp_slow_start_after_idle = 0

# Increase Linux autotuning TCP buffer limits
# Set max to 16MB for 1GE and 32M (33554432) or 54M (56623104) for 10GE
# Don't set tcp_mem itself! Let the kernel scale it based on RAM.
# net.core.rmem_max = 16777216
# net.core.wmem_max = 16777216
# net.core.rmem_default = 16777216
# net.core.wmem_default = 16777216
# net.core.optmem_max = 40960
# net.ipv4.tcp_rmem = 4096 87380 16777216
# net.ipv4.tcp_wmem = 4096 65536 16777216


# --------------------------------------------------------------------
# The following allow the server to handle lots of connection churn
# --------------------------------------------------------------------

# Disconnect dead TCP connections after 1 minute
net.ipv4.tcp_keepalive_time = 60

# Wait a maximum of 5 * 2 = 10 seconds in the TIME_WAIT state after a FIN, to handle
# any remaining packets in the network.
net.ipv4.netfilter.ip_conntrack_tcp_timeout_time_wait = 5

# Allow a high number of timewait sockets
net.ipv4.tcp_max_tw_buckets = 2000000

# Timeout broken connections faster (amount of time to wait for FIN)
net.ipv4.tcp_fin_timeout = 10

# Let the networking stack reuse TIME_WAIT connections when it thinks it's safe to do so
# net.ipv4.tcp_tw_reuse = 1

# Determines the wait time between isAlive interval probes (reduce from 75 sec to 15)
net.ipv4.tcp_keepalive_intvl = 15

# Determines the number of probes before timing out (reduce from 9 sec to 5 sec)
net.ipv4.tcp_keepalive_probes = 5

# -------------------------------------------------------------