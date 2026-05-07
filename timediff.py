#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess
from mtm_pyutils.zeitRegex import createTimestring
from mtm_pyutils.gt10sek import gt10sekInFuture
import sqlite3

# wir holen uns den letzten Messwert und nehmen ihn als Richtlinie für die 
# Kompensation der Zeit bei der gestoppt werden soll.
verbindung=sqlite3.connect("/home/harry/.mtm/muehle.db")
zeiger=verbindung.cursor()
zeiger.execute("SELECT timedelta FROM muehle ORDER BY date DESC, time DESC LIMIT 1;")
inhalt=zeiger.fetchall()
verbindung.close()
inhalt=inhalt[0][0] # fetchall gibt ein Tupel (nur index 0 belegt?!) in einer Liste zurück e.g. [(wert, )]

def strtotmestmp(timestring): # string to timestamp -> takes a HH:MM:SS string and
                              # converts it to an unix-timestamp
  return datetime.combine(datetime.now().date(), \
         datetime.strptime(timestring, '%H:%M:%S').time()).timestamp()

sollZeit=gt10sekInFuture(inhalt)

# wir rechnen hier mit der Unix-Zeit. Zeit des Programmstarts minus
# den gemessenen Wert (.timestamp = UNIX TIME)
unixtime_eingabe=strtotmestmp(sollZeit)

satisfied=False

while not satisfied:

  keyPressed=input('Drücken Sie exakt um %s Uhr eine beliebige Taste...' % sollZeit)

  unixtime_now=datetime.now().timestamp()

  diff=unixtime_eingabe-unixtime_now

  jaSager=['y', 'Y', 'Yes', 'YES', 'yes', 'j', 'J', 'Ja', 'ja']

  wiederholer=['a', 'A', 'again', 'Again', 'n', 'N', 'nein', 'Nein', 'no', 'No', 'NEIN', 'NO']

  finish=['q', 'Q', 'Quit', 'quit', 'QUIT']

  print('Abweichung zur Referenzzeit: %.1f Sekunden.' % diff)
  question=input('Ergebnis in Datenbank speichern? ([y]es / [a]gain / [q]uit): ')
  if question in jaSager:
    break

  if question in wiederholer:
    neuerEingabestring=gt10sekInFuture(inhalt)
    sollZeit=neuerEingabestring
    unixtime_eingabe=strtotmestmp(neuerEingabestring)
    
  if question in finish:
    sys.exit(0)

subprocess.run(['./mtm.sh', '-x %.1f' % diff], check=True)
