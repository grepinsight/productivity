#!/bin/bash
# git_blameable.sh <Author> <file>


if grep -l "$1" <(git blame "$2") > /dev/null; then
	echo "$2"
fi


