I get it. `systemd` is really complex and confusing. A lot of people, including
myself, learn best by example. I'm basically just a glorified script kiddie.

# Quick Info

* You want to put _`your.service`_ file in the directory returned by
  **`pkg-config systemd --variable systemdsystemunitdir`**. Any time you add,
  edit, or remove files under here, you must call **`systemctl daemon-reload`**
  or systemd will complain.

* `ExecStart` and `ExecStop` are executed directly, not via a shell. `systemd`
  has a [shitty parameter expansion feature](https://unix.stackexchange.com/a/216786/128494)
  and it might make you think that it supports all of your shell's features.
  Protip: [it doesn't](https://www.freedesktop.org/software/systemd/man/systemd.service#Command%20lines).
  If you want something complex, put it into a shell script with a [shebang](https://en.wikipedia.org/wiki/Shebang_%28Unix%29))
  and execute the absolute path. Bash, Python, and PHP files prefixed with a
  shebang work wonders here! Call the absolute path and make sure your script is
  executable (`chmod +x`).

* You want to make sure your programs aren't running as root if they don't need
  to. Fill out the [`User=`](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#User=)
  field in the `[Service]` section. Make sure to `adduser` the name if you've
  haven't already. [`DynamicUser=`](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#DynamicUser=)
  sounds good but you're probably going to have all kinds of trouble with
  filesystem permissions and `systemd` adds a bunch of other "oh yeahs" in an
  effort to fix up security problems (because `systemd` doesn't follow the Unix
  principle of "do one thing and do it well").

* Debug your shit with **`systemctl status -l --no-pager` _`your.service`_** and
  **`journalctl -l --no-pager -u` _`your.service`_**. The `--no-pager` bit is
  important if you're writing scripts because `systemd` changes its output based
  on whether you're attached to a tty and makes it a royal pain in the ass to
  write a script. The `-l` tells `systemd` not to truncate your logs for the
  same reason.

# Examples

* `tmux` with `systemd` is a pretty handy piece of duct tape for programs that
  want a terminal window that you want to have available at startup.

    * Start a TMUX session as my user at boot and `echo hello world` into it.

        * [tmux-hello-world](tmux-hello-world)

    * Some programs write log to stdout or stderr and don't have a way to
        configure a log file. Some other programs are interactive.

        `tmux` is a pretty handy wrapper for stuff like that. I particularly like
        to have a `tmux` session for such a program with one pane running that
        program in one window while piping the stdout and stderr through `tee` to
        some log files. Another scenario I've seen work well is to pipe the output
        directly to a log file and have another pane or two to just `tail` those
        files.

* `sshfs` is cool. Use `systemd` to mount `ssh`/`sftp`-accessible stuff at boot.

    * A bunch of options are inherited from `ssh_config`. Some of the more
      useful options:

        * `_netdev`: [tells systemd that it's a network mount](https://unix.stackexchange.com/a/331688/128494).
          That's important so that it doesn't hang at boot when trying to mount
          things more the network interfaces are online.
        * `Port=22`: connect to the SSH server on this TCP port.
        * [Automatically reconnecting](https://serverfault.com/a/639735/245340)
          is useful. If the connection dies with outstanding IO, the process(es)
          with open files should see an error indication from their file
          descriptor.
            * `reconnect`: `sshfs` will automatically reconnect if the
              connection dies.
            * `ServerAliveInterval=15`: after 15 seconds of no network activity,
              send a ping to the server on the ssh protocol.
            * `ServerAliveCountMax=3`: after 3 missed ssh-protocol pings,
              consider the connection to be dead.
        * Authentication is important.
            * `IdentityFile=/path/to/secret/key`: authorize using the specified
              encryption key. I'm not sure how to specify a passphrase to unlock
              it if one is necessary. I believe the key will be accessed using
              the root user.
        * You could consider `sshfs` to work in two "modes". The first mode
            allows the local access to the remote only by the user who set up
            the connection. The second allows access based on matching the
            UID/GID of the local and remote; no mapping is done, so there's a
            one-to-one exact match.
            * `allow_other`: [opt-in to the kernel's FUSE driver to perform UID/GID permission validation](https://serverfault.com/a/294120/245340).
            You might also [need to set `user_allow_other` in `/etc/fuse.conf`](https://superuser.com/a/262800/403994).

    * At my local `/mnt/remote/fsroot` -> mount the ssh-remote
        `user@192.168.1.1:/` -> authorized by SSH key at
        `/root/.ssh/user@192.168.1.1.id_rsa`.
        * [sshfs-mount-root](sshfs-mount-root)

Want to add your own examples? Create a [pull request](https://github.com/inetknght/systemd.software).
