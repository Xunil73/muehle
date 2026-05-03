#!/usr/bin/env python3

import sys
import re

def createTimestring():
  arg=sys.argv[1]

  pattern=[ r'^[0-9][0-9]$',\
            r'^[0-9][0-9][0-9][0-9]$',\
            r'^[0-9][0-9][0-9][0-9][0-9][0-9]$',\
            r'^[0-9][0-9]:[0-9][0-9]$',\
            r'^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$' ]

  for i, ele in enumerate(pattern):
    if re.match(ele, arg):
      if i == 0:
        arg=arg+':00:00'
      if i == 1:
        arg=arg[:2]+':'+arg[2:]+':00'
      if i == 3:
        arg=arg[:2]+':'+arg[2:4]+':'+arg[4:]
# here continue.... (and test the above)
    re.match(ele, arg) and print("auch das geht...")

  print(arg)
createTimestring()
