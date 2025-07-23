#!/usr/bin/env bash



CURRENT_ZOOM_MTG="$(gfind $HOME/Documents/Zoom -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -d' ' -f2-)"


cat "$CURRENT_ZOOM_MTG" | fabric -p summarize_lecture -m gpt-4o

