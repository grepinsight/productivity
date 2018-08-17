#!/bin/bash


if grep -l --file=<(git log dev..$(git rev-parse --abbrev-ref HEAD) --oneline | awk '{print $1}') <(git blame "$2") > /dev/null; then
	echo "$2"
fi


