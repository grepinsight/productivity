#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# From https://gist.github.com/EinfachToll/9071573
#
# Put this file anywhere and add the following to your .vimrc.
# The value of ctagsargs must be one of 'default', 'markdown' or 'media'.
#
# let g:tagbar_type_vimwiki = {
#             \   'ctagstype':'vimwiki'
#             \ , 'kinds':['h:header']
#             \ , 'sro':'&&&'
#             \ , 'kind2scope':{'h':'header'}
#             \ , 'sort':0
#             \ , 'ctagsbin':'https://gist.github.com/EinfachToll/9071573'
#             \ , 'ctagsargs': 'default'
#             \ }

import sys
import re

syntax = sys.argv[1]
filename = sys.argv[2]

if syntax == "default" or syntax == "media":
    rx_header = re.compile(r"^\s*(={1,6})([^=].*[^=])\1\s*$")
elif syntax == "markdown":
    rx_header = re.compile(r"^\s*(#{1,6})([^#].*)$")

file_content = []
with open(filename, "r") as vim_buffer:
    file_content = vim_buffer.readlines()

state = [""]*6
print("HI")
for lnum, line in enumerate(file_content):

    match_header = rx_header.match(line)

    if not match_header:
        continue

    cur_lvl = len(match_header.group(1))
    cur_tag = match_header.group(2).strip()
    cur_searchterm = "^" + match_header.group(0).rstrip("\r\n") + "$"
    cur_kind = "h"

    state[cur_lvl-1] = cur_tag
    for i in range(cur_lvl, 6):
        state[i] = ""

    scope = "&&&".join([ state[i] for i in range(0, cur_lvl-1) if state[i] != "" ])
    if scope:
        scope = "\theader:" + scope

    print('{0}\t{1}\t/{2}/;"\t{3}\tline:{4}{5}'.format(cur_tag, filename,
            cur_searchterm, cur_kind, str(lnum+1), scope))
