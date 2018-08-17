#! /usr/bin/env bash

hi_color=$(tput setaf 4) #blue
bold=$(tput bold)
underline=$(tput smul)
normal=$(tput sgr0)

read -r -d '' usage << DOC
Prints out a table of tmux sessons, windows, and panels.

Active panes appear in ${hi_color}color${normal}.
Attached panes are ${bold}${hi_color}bolded${normal}.
The current pane will be ${underline}${bold}${hi_color}underlined${normal} if this shell is in a tmux session.
DOC


if [ "$1" = "-h"  -o "$1" = "--help" ]
then
	printf "%s\n" "$usage"
	exit
fi

# Exit if tmux is not running
tmux has || exit 1

pane_arr=()
format_arr=()

format="%s	%s	%s	%s	%s	%s"
pane_arr+=( "$(printf "$format" ID "Session Start" Session Window Pane Path)" )

# See FORMAT section of tmux's man page
tmux_args="'#{session_id}:#{window_id}:#{pane_id}' '#{session_name}' "
tmux_args+="#{session_created} '#{window_index}:#{window_name}#{window_flags}' "
tmux_args+="'#{pane_index}:#{pane_current_command}' '#{pane_current_path}' "
tmux_args+="#{session_attached} #{window_active} #{pane_active}"

# Parse output line by line
{ while read -r str_args
	do
	# Parse quoted arguments
	declare -a "args=($str_args)"
	TMUX_ID=${args[0]}
	SESSION=${args[1]}
	SESSION_TIME=${args[2]}
	WINDOW=${args[3]}
	PANE=${args[4]}
	PANE_PATH=${args[5]}
	SESSION_ATTACHED=${args[6]}
	WINDOW_ACTIVE=${args[7]}
	PANE_ACTIVE=${args[8]}

	SESSION_TIME=$(gdate -d @$SESSION_TIME +"%d %b %R") # Jan 01 hh:mm format
	color=""

	# Highlight only the active panes in active windows
	if [ "$PANE_ACTIVE" == "1" -a "$WINDOW_ACTIVE" == "1" ]
	then
		color="${hi_color}$color"
		# Bold (embolden?) active panes in attached sessions
		if [ "$SESSION_ATTACHED" == "1" ]
		then
			color="${bold}$color"
			# Underline the pane that is active in this terminal 
			if [[ "$TMUX_ID" == *":$(tmux display -p "#D")" ]] && [ -n "$TMUX" ]
			then
				color="${underline}$color"
			fi
		fi
	fi
	format_arr+=( "$color" )
	pane_arr+=( "$(printf "$format" "$TMUX_ID" "$SESSION_TIME" "$SESSION" "$WINDOW" "$PANE" "$PANE_PATH")" )
done
} < <(tmux list-panes -aF "$tmux_args")
output=()
OIFS=$IFS
IFS=$'\n'
{ while read -r line; do output+=( "$line" ); done } < <({ for line in ${pane_arr[@]}; do echo "$line"; done } | column -t -s $'\t')
IFS=$OIFS

{ for i in $(seq 0 "${#output[@]}"); do
	closing_format=""
	if [ -n "${format_arr[$i]}" ]
	then closing_format="${normal}"
	fi
	printf "%s%s%s\n" "${format_arr[$i]}" "${output[$i]}" "$closing_format"
done }

