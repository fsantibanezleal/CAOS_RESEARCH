#!/bin/bash
# usage: launch_singular.sh PIDFILE SINGFILE   (records its own pid so that the Python driver can kill exactly this process)
echo $$ > "$1"
exec Singular -q < "$2"
