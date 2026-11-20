#!/bin/bash
# usage: launch.sh PIDFILE SCRIPT ARG...   (records its own pid so that the Python driver can kill exactly this process)
pidfile="$1"; shift
echo $$ > "$pidfile"
exec M2 --script "$@"
