#!/bin/bash



if is_git_dir; then
    ag '\[ \]' --md
fi
