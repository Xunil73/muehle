#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess
from mtm_pyutils.zeitRegex import createTimestring
from mtm_pyutils.gt10sek import gt10sekInFuture


sollZeit=gt10sekInFuture()

# wir rechnen hier mit der Unix-Zeit. Zeit des Programmstarts minus
# den gemessenen Wert (.timestamp = UNIX TIME)
unixtime_eingabe=datetime.combine(datetime.now().date(), \
                 datetime.strptime(sollZeit, '%H:%M:%S').time()).timestamp()

zufrieden=False

while not zufrieden:

  keyPressed=input('Drücken Sie exakt um %s Uhr eine beliebige Taste...' % sollZeit)

  unixtime_now=datetime.now().timestamp()

  diff=unixtime_eingabe-unixtime_now

  jaSager=['y', 'Y', 'Yes', 'YES', 'yes', 'j', 'J', 'Ja', 'ja']

  wiederholer=['n', 'N', 'nein', 'Nein', 'no', 'No', 'NEIN', 'NO']

  rausschmeisser=['q', 'Q', 'Quit', 'quit', 'QUIT']

  print('Abweichung zur Referenzzeit: %.1f Sekunden.' % diff)
  umfrage=input('Ergebnis in Datenbank speichern? ([y]es/[n]ochmal/[q]uit)')
  if umfrage in jaSager:
    break

  if umfrage in wiederholer:
    neuerEingabestring=gt10sekInFuture()
    sollZeit=neuerEingabestring
    unixtime_eingabe=datetime.combine(datetime.now().date(), \
                     datetime.strptime(neuerEingabestring, '%H:%M:%S').time()).timestamp()
    
  if umfrage in rausschmeisser:
    sys.exit(0)

subprocess.run(['./mtm.sh', '-x %.1f' % diff], check=True)
