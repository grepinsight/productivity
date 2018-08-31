#!/bin/bash

if which pmset >/dev/null; then
	pmset -g batt | grep Internal | egrep -o '[0-9]+%.*' | perl -ne 'm/(\d+)%.*(\d+:\d+)/;print "$1%| $2h use"'
fi
