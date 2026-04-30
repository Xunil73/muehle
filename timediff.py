#!/usr/bin/env python3

import sys
from datetime import datetime


unixtime_eingabe=datetime.combine(datetime.now().date(), \
                 datetime.strptime(sys.argv[1], '%H:%M:%S').time()).timestamp()

zufrieden=False

while not zufrieden:

  keyPressed=input('Drücken Sie exakt um %s Uhr eine beliebige Taste...' % sys.argv[1])

  unixtime_now=datetime.now().timestamp()

  diff=unixtime_eingabe-unixtime_now

  print(diff)
  print('%.1f' % diff )

  jaSager=['y', 'Y', 'Yes', 'yes', 'j', 'J', 'Ja', 'ja']
  umfrage=input('Wollen Sie dieses Ergebnis verwenden? (y/n)')
  if umfrage in jaSager:
    break

print('Programmende')
