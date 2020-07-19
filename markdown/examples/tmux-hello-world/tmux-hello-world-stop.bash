#!/usr/bin/env bash

set -xeuo pipefail

#
# Read this from `journalctl --no-pager -u tmux-hello-world.service` or also
# `systemctl status --no-pager tmux-hello-world.service`.
echo "I am running as $(whoami) and I am killing a tmux session. I hope I said hello!"

if tmux has-session -t tmux-hello-world
then
	tmux kill-session -t tmux-hello-world
fi
