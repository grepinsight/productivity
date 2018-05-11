#!/bin/bash

if which $1; then
    vim $(which $1)
else
    echo "$1 does not exist in PATH"
fi
