#!/usr/bin/env bash

set -xeuo pipefail

#
# Read this from `journalctl --no-pager -u tmux-hello-world.service` or also
# `systemctl status --no-pager tmux-hello-world.service`.
echo "I am running as $(whoami) and I am starting a tmux session to say hello!"

if ! tmux has-session -t tmux-hello-world
then
  tmux new-session -d -s tmux-hello-world
  #
  # Type out the command into the bash prompt.
  tmux send-keys -t tmux-hello-world -l "echo hello world"
  #
  # Press enter.
  tmux send-keys -t tmux-hello-world "Enter"
else
  # The session is already running. You might have attached to it and have
  # something typed up. You might even be attached and typing  _right now_!
  # I don't want to interrupt you. So I'll just log an error message.
  #
  # You can see this error message in `journalctl -u tmux-hello-world.service`
  # or also `systemctl status --no-pager tmux-hello-world.service`.
  >&2 echo "My tmux-hello-world session is already running!"
  >&2 echo "I don't want to be overly greety so I won't say hello."
  exit 1
fi
