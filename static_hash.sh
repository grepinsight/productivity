#!/bin/bash

# Usage:
# get_hash "https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css"
# get_hash "https://maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css"
# get_hash "https://igv.org/web/release/1.0.9/igv-1.0.9.css"
# get_hash "http://igv.org/web/examples/css/bam.css"
# get_hash "https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js"
# get_hash "https://igv.org/web/release/1.0.9/igv-1.0.9.js"





function get_hash {
  curl -O $1 2>/dev/null
  resource_name=$(basename $1)
  ext=${resource_name##*.}
  integrity=$(cat $resource_name | openssl dgst -sha384 -binary | openssl enc -base64 -A)
  
  # if css
  if [[ ${ext} == "css" ]]; then
    echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"$1\" integrity=\"sha384-${integrity}\" crossorigin=\"anonymous\">"
  fi

  # if js
  if [[ ${ext} == "js" ]]; then
    echo "<script src=\"$1\" integrity=\"sha384-${integrity}\" crossorigin=\"anonymous\"></script>"
  fi
}

get_hash "$1"
