#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

help_text = """
Extracts tags from rmd files. Useful for the Tagbar plugin.

Usage:
Install Tagbar (http://majutsushi.github.io/tagbar/). Then, put this file
anywhere and add the following to your .vimrc:

let g:tagbar_type_rmd = {
          \   'ctagstype':'rmd'
          \ , 'kinds':['h:header', 'c:chunk', 'f:function', 'v:variable']
          \ , 'sro':'&&&'
          \ , 'kind2scope':{'h':'header', 'c':'chunk', 'f':'function', 'v':'variable'}
          \ , 'sort':0
          \ , 'ctagsbin':'/path/to/rmdtags.py'
          \ . 'ctagsargs':''
          \ }
"""

import sys
import re

if len(sys.argv) < 2:
    print(help_text)
    exit()

filename = sys.argv[1]

# filename = "test.Rmd"
print(filename)

re_header = re.compile(r"^(#+)([^{]+)(\{[^}]+\})?$")
re_chunk = re.compile(r"^```\{r ([^,]+)(,[^}]*)?\}$")
re_function = re.compile(r"^[\t ]*([^ ]+) *<- *function.*$")
re_variable1 = re.compile(r"^[\t ]*([^ ]+) *<-.*$")
re_variable2 = re.compile(r"^.*-> *(.+)$")

file_content = []
try:
    with open(filename, "r") as vim_buffer:
        file_content = vim_buffer.readlines()
except:
    exit()

headers = []
depth = [0]
inChunk = False
curChunk = None
for lnum, line in enumerate(file_content):
    newline = []
    tag = ""
    signature = ""
    options = ""
    # Headers
    if re_header.match(line) and not inChunk:
        level = len(re_header.match(line).group(1))
        tag = re_header.match(line).group(2).strip()
        newline.append(tag)
        newline.append(filename)
        newline.append('/^' + line.rstrip("\n") + '$/;"')
        newline.append("h")
        newline.append("line:" + str(lnum+1))
        # header
        while (level <= depth[len(depth) -1]):
            headers.pop()
            depth.pop()
        if len(headers) > 0:
            options = "header:" + "&&&".join(headers)
        headers.append(tag)
        depth.append(level)
        # signature
        if re_header.match(line).group(3):
            signature = "(" + re_header.match(line).group(3).strip("{}") + ")"
            options = options + "\tsignature:" + signature
        # Print
        newline.append(options)
        print("\t".join(newline))
    # Chunks
    if re_chunk.match(line):
        inChunk = True
        curChunk = re_chunk.match(line).group(1).strip()
        newline.append(re_chunk.match(line).group(1).strip())
        newline.append(filename)
        newline.append('/^' + line.rstrip("\n") + '$/;"')
        newline.append("c")
        newline.append("line:" + str(lnum+1))
        if len(headers) > 0:
            options = "header:" + "&&&".join(headers)
        if re_chunk.match(line).group(2):
            signature = "(" + re_chunk.match(line).group(2).lstrip(", ") + ")"
            options = options + "\tsignature:" + signature
        # Print
        newline.append(options)
        print("\t".join(newline))
    if line == "```\n":
        inChunk = False
        curChunk = None
    # Functions
    if re_function.match(line) and inChunk:
        newline.append(re_function.match(line).group(1).strip())
        newline.append(filename)
        newline.append('/^' + line.rstrip("\n") + '$/;"')
        newline.append("f")
        newline.append("line:" + str(lnum+1))
        print("\t".join(newline))
    elif (re_variable1.match(line) or re_variable2.match(line)) and inChunk:
        tag = re_variable1.match(line) or re_variable2.match(line)
        tag = tag.group(1).strip()
        newline.append(tag)
        newline.append(filename)
        newline.append('/^' + line.rstrip("\n") + '$/;"')
        newline.append("v")
        newline.append("line:" + str(lnum+1))
        print("\t".join(newline))

