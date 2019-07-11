#!/bin/bash

set -eux


contents=$(find /Users/allee/Desktop/ -type f -name 'Screen*png' -print0)

if [[ -n "$contents" ]]; then
	find ~/Desktop/ -type f -name "Screen*png" -print0 | xargs -0 rm
fi
