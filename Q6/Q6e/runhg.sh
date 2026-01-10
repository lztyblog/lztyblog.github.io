#!/bin/sh
timeout -s SIGINT 5s stdbuf -oL valgrind --log-fd=1 --tool=helgrind "$1" | sed -E 's|/home/([^/]*/)+|<path>/|g'
