#!/usr/bin/env python3

import sys
import re

# Funktion erzeugt aus einer Zeiteingabe (hh, hhmm, hhmmss, hh:mm, hh:mm:ss) einen vollständigen
# String mit der Uhrzeit -> hh:mm:ss
def createTimestring(tme):
  arg=tme

  pattern=[ r'^[0-9][0-9]$',\
            r'^[0-9][0-9][0-9][0-9]$',\
            r'^[0-9][0-9][0-9][0-9][0-9][0-9]$',\
            r'^[0-9][0-9]:[0-9][0-9]$',\
            r'^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$',\
            r'.*' ]

  for i, ele in enumerate(pattern):
    if re.match(ele, arg):
      if i == 0:
        arg=arg+':00:00'
      if i == 1:
        arg=arg[:2]+':'+arg[2:]+':00'
      if i == 2:
        arg=arg[:2]+':'+arg[2:4]+':'+arg[4:]
      if i == 3:
        arg=arg+':00'
      if i == 4:
        break
      if i == 5:
        print('pymtm: kann Argument nicht verarbeiten')
        sys.exit(-1)
    re.match(ele, arg) and print("auch das geht...")

  return arg
