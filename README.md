# [`systemd.software`](https://github.com./inetknght/systemd.software)

I am a software developer by nature and a system administrator by necessity. As
such I find `systemd` to be far too complex for my taste. I learn by doing: I
copy examples and then read documentation about things used before adjusting
what gets pasted.

I also find `systemd` documentation to be a nightmare. In particular, the url to
the documentation on freedesktop.org is annoying to type or remember. So
instead, I figure it'd be handy to have a shorter URL to remember.

I also included some [examples](https://systemd.software/examples) for using
`systemd` to augment your software on Linux. Eventually I'll write a generator
for wrapping applications into common configurations that are described in the
examples.

[This repository](https://github.com./inetknght/systemd.software) contains
artifacts for the [`systemd.software`](https://systemd.software/) web redirector
service, templates, examples, and configuration for the domain.

# instructions common to all or most configuration files

[https://systemd.software/directives](https://systemd.software/directives)

`systemd` configuration files follow a syntax similar to INI files. A lot of the
types of configuration files have common parameters. Instead of duplicating the
documentation everywhere, those common parameters are described under the
"directives" section.

## Basic service file documentation

[https://systemd.software/services](https://systemd.software/services)

Services tell `systemd` how to run a program. The program could be long-running
like a daemon but doesn't have to be. It can be configured to run automatically
at boot or as a dependency when another service starts up. It can be
automatically restarted. You can tell it what environment variables to use.

## Socket service file documentation

[https://systemd.software/sockets](https://systemd.software/sockets)

`systemd` is capable of setting up listening sockets and then starting your
programs on-demand instead of pre-emptively. These types of services are
described by `.socket` files. These are configuration files, not [Unix Socket
Domain](https://en.wikipedia.org./wiki/Unix_domain_socket) socket files so don't
get confused by the file suffix.

Frankly I haven't used these so I'm not totally
familiar with getting them working. Please help by creating a
[pull request](https://github.com./inetknght/systemd.software) with example(s)!
I'd be particularly interested in learning how to use this with Unix Domain
Sockets.

## Filesystem mount documentation

[https://systemd.software/mounts](https://systemd.software/mounts)

`systemd` can be used to describe your filesystems. That's handy, I guess.
Mounts are another thing I've never used. But I'm pretty interested to learn
if it can handle loopback devices to an image. If so I'll probably add an
example for a `fedora.iso` and a `raspbian.img`, since those are particularly
relevant to my interests. I'm also interested in learning if it can be used to
manage `sshfs` mounts.

I assume it can manage your typical nonsense like `nfs`, `ext4`, `ntfs`, and
`luks`. But you know what they say about assumptions.

## Automatically-mounted filesystems

[https://systemd.software/automounts](https://systemd.software/automounts)

Apparently `systemd` mounts... aren't automatically mounted? That seems dumb.
So there's these `.automount` to solve that. I don't know why that's not part
of `.mount`. Who the hell made this shit up?

## "Links" (networks)

[https://systemd.software/links](https://systemd.software/links)

I frequently forget that NetworkManager's `nmcli` isn't part of `systemd`.
Indeed, `systemd` describes networks using `.link` files. I've read that there's
a lot of strife between the two types of network management services.

Frankly I think `nmcli` is garbage. But I've already learned it enough to use it
passably. I hope `.link` is easier. I miss `ifup` and `ifdown` scripts :'(

If it makes it easier to manage a [WireGuard](https://wireguard.com./) interface
that'd be great.

# `systemd` commands

## `systemctl` - Manage your OS.

[https://systemd.software/systemctl](https://systemd.software/systemctl)

`systemctl` is used to manage your OS. It comes in two parts; primarily it
manages the services. Secondarily you use it it to tell your physical machine
to reboot.

### Service Statuses

* `enabled`: service will start automatically (at boot or when needed)
* `disabled`: service will not start automatically (unless it's a dependency)
* `masked`: service will refuse to start (even if it's a dependency)
* `unmasked`: opposite of masked
* `started`: service is running
* `stopped`: service _was_ running but finished.
* `error`: service started but exited for a reason that its unit file describes
  as a failure. If any service is in this state, then `systemctl status` will
  show `State: degraded`. Figuring out what service(s) failed isn't intuitive.
* `inactive`: uhhh I think it's just another word for "not started"? I'm not
  sure

`systemctl` _can_ be used to look at the logs for individual services. But
`journalctl` is a better tool for that.

### tl;dr

* system status: `systemctl status --no-pager`
* show failed services: `systemctl --state=failed --no-pager`
* clear failure state of service: `systemctl reset-failed unit.service`
  ([from Unix StackExchange](https://unix.stackexchange.com/a/418797/128494))
* reboot: `systemctl reboot --now`

## `journalctl` - Logs.

[https://systemd.software/journalctl](https://systemd.software/journalctl)

`journalctl` manages the _system journal_. The journal is just a fancy way of
saying logs. Why not use the word `diary` instead? Whatever.

tl;dr:

* Specific service's logs: `journalctl -u unit.service`
* All logs since current boot: `journalctl -b --no-pager`
* List what boots still have logs: `journalctl --list-boots`

Stupid people use `-x`.

## `machinectl` - Virtual Machine and Container management

[https://systemd.software/machinectl](https://systemd.software/machinectl)

`machinectl` manages... "machines"; virtual machines and containers. I've never
used it. Feel free to add some examples: I'm quite interested in learning
competitors to VirtualBox.

## `networkctl` - NIC management (competes with Network Manager's `nmcli`)

[https://systemd.software/networkctl](https://systemd.software/networkctl)

`networkctl` competes with Network Manager. I haven't used it. It looks like it
works with the [`.link`](https://systemd.software/links) files.

## `resolvectl` - Control how your DNS works

[https://systemd.software/resolvectl](https://systemd.software/resolvectl)

The system resolver is way more complicated than it needs to be. It's especially
confounding when you're using Docker to build images -- Docker makes its own
`/etc/resolv.conf` file inside of the containers. GRRRRR

# Things that aren't actually part of `systemd`

`systemd` has, in my opinion by its very name and stated goals, convoluted what
other system services are and can do.

## `nmcli` - Network Manager (CLI)

[https://systemd.software/nmcli](https://systemd.software/nmcli)

Network Manager organizes NICs into _Layer 2 physical devices_ and _Layer 3
logical connections_. Generally think of them as layer 2 can be powered on or
off, plugged in or not, etc while layer 3 controls IP configuration. You "can"
change the layer 3 configuration without changing the layer 2 status.

### tl;dr

`nmcli` is bash autocompletion friendly.

Changes made to configurations are not applied immediately. If you change
something then it's easiest to bring the device or connection offline and then
back online.

* show layer 2 device status: `nmcli d`
* show layer 3 connection status: `nmcli c`
* bring device (and connection) offline: `nmcli d disconnect <device>`
* bring connection (not device) offline: `nmcli c down <connection>`
* show device configuration: `nmcli d show <device>`
* show connection config: `nmcli c show <connection>`

## `firewalld` - "Dynamic Firewall Manager"

[https://systemd.software/firewalld](https://systemd.software/firewalld)
