#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess

unixtime_eingabe=datetime.combine(datetime.now().date(), \
                 datetime.strptime(sys.argv[1], '%H:%M:%S').time()).timestamp()

zufrieden=False

while not zufrieden:

  keyPressed=input('Drücken Sie exakt um %s Uhr eine beliebige Taste...' % sys.argv[1])

  unixtime_now=datetime.now().timestamp()

  diff=unixtime_eingabe-unixtime_now

  #print(diff)
  #print('%.1f' % diff )

  jaSager=['y', 'Y', 'Yes', 'YES', 'yes', 'j', 'J', 'Ja', 'ja']
  rausschmeisser=['q', 'Q', 'Quit', 'quit', 'QUIT']
  umfrage=input('Wollen Sie dieses Ergebnis verwenden? (y/n/[q]uit)')
  if umfrage in jaSager:
    break
  if umfrage in rausschmeisser:
    sys.exit(0)

subprocess.run(['./mtm.sh', '-x %.1f' % diff], check=True)
