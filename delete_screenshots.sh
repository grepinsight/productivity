#!/bin/bash

set -eux


contents=$(find /Users/allee/Desktop/ -type f -name 'Screen*png' -print0)

if [[ ! -z $contents ]]; then
	find ~/Desktop/ -type f -name "Screen*png" -print0 | xargs -0 rm
fi
