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

# Basic service file documentation

[https://systemd.software/services](https://systemd.software/services)

Services tell `systemd` how to run a program. The program could be long-running
like a daemon but doesn't have to be. It can be configured to run automatically
at boot or as a dependency when another service starts up. It can be
automatically restarted. You can tell it what environment variables to use.

# Socket service file documentation

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

# Filesystem mount documentation

[https://systemd.software/mounts](https://systemd.software/mounts)

`systemd` can be used to describe your filesystems. That's handy, I guess.
Mounts are another thing I've never used. But I'm pretty interested to learn
if it can handle loopback devices to an image. If so I'll probably add an
example for a `fedora.iso` and a `raspbian.img`, since those are particularly
relevant to my interests. I'm also interested in learning if it can be used to
manage `sshfs` mounts.

I assume it can manage your typical nonsense like `nfs`, `ext4`, `ntfs`, and
`luks`. But you know what they say about assumptions.

# Automatically-mounted filesystems

[https://systemd.software/automounts](https://systemd.software/automounts)

Apparently `systemd` mounts... aren't automatically mounted? That seems dumb.
So there's these `.automount` to solve that. I don't know why that's not part
of `.mount`. Who the hell made this shit up?

# "Links" (networks)

[https://systemd.software/links](https://systemd.software/links)

I frequently forget that NetworkManager's `nmcli` isn't part of `systemd`.
Indeed, `systemd` describes networks using `.link` files. I've read that there's
a lot of strife between the two types of network management services.

Frankly I think `nmcli` is garbage. But I've already learned it enough to use it
passably. I hope `.link` is easier. I miss `ifup` and `ifdown` scripts :'(

If it makes it easier to manage a [WireGuard](https://wireguard.com./) interface that'd be great.
