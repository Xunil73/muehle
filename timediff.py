#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess
from zeitRegex import createTimestring

sollZeit=createTimestring(sys.argv[1])

# wir rechnen hier mit der Unix-Zeit. Zeit des Programmstarts minus
# den gemessenen Wert (.timestamp = UNIX TIME)
unixtime_eingabe=datetime.combine(datetime.now().date(), \
                 datetime.strptime(sollZeit, '%H:%M:%S').time()).timestamp()

zufrieden=False

while not zufrieden:

  keyPressed=input('Drücken Sie exakt um %s Uhr eine beliebige Taste...' % sys.argv[1])

  unixtime_now=datetime.now().timestamp()

  diff=unixtime_eingabe-unixtime_now

  print('%.1f Abweichung...' % diff )

  jaSager=['y', 'Y', 'Yes', 'YES', 'yes', 'j', 'J', 'Ja', 'ja']
  rausschmeisser=['q', 'Q', 'Quit', 'quit', 'QUIT']
  umfrage=input('Wollen Sie dieses Ergebnis verwenden? (y/n/[q]uit)')
  if umfrage in jaSager:
    break
  if umfrage in rausschmeisser:
    sys.exit(0)

subprocess.run(['./mtm.sh', '-x %.1f' % diff], check=True)
