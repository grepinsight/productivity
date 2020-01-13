#!/bin/bash

set -eux


contents=$(find /Users/allee/Desktop/ -type f -name 'Screen*png' -print0)

mkdir -p $HOME/Desktop/screenshots

if [[ -n "$contents" ]]; then
	find ~/Desktop/ -type f -name "Screen*png" -print0 | xargs -0 -I{} mv {} $HOME/Desktop/screenshots/
fi
