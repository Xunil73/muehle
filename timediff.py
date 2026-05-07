#!/usr/bin/env python3

import sys
from datetime import datetime
import subprocess
from mtm_pyutils.zeitRegex import createTimestring
from mtm_pyutils.gt10sek import gt10sekInFuture
import sqlite3
import argparse

# damit wandeln wir einen String mit Uhrzeit in einen Zeitstempel im UNIX Format.
def strToTimestamp(timestring):
  return datetime.combine(datetime.now().date(), \
         datetime.strptime(timestring, '%H:%M:%S').time()).timestamp()


parse=argparse.ArgumentParser()
parse.add_argument('-n', '--no-compensation',\
                   dest='nocompensation',\
                   action="store_true",\
                   help="next measure point is computed from system's clock, not testwatch")
args=parse.parse_args()

# wir lesen den Inhalt der mtm.conf und wissen wo die Datenbank ist und wie 
# sie heisst.
conffile=open('/home/harry/.mtm/mtm.conf', 'r')
conftext=conffile.read().strip() # strip notwendig da sqlite3.connect() sonst wegen eines 
conffile.close()                 # Zeilenumbruchzeichens in der .conf die Datenbank nicht finden kann.

# wir holen uns den letzten Messwert und nehmen ihn als Richtlinie für die 
# Kompensation der Zeit bei der gestoppt werden soll.
# Vorher habe ich die Systemzeit des Computers als Startpunkt genommen, dann bis zu den nächsten
# fünf vollen Sekunden aufgefüllt und nochmal zehn addiert. Die Praxis hat gezeigt dass, im Falle die 
# Testuhr geht 30 Sekunden nach, dies einen zu langen Zeitraum dauert bis man an den Messpunkt kommt.
# Umgekehrt gilt, die Zeit zum Messpunkt wird unpraktikabel kurz wenn die Uhr deutlich vor geht.
# Deshalb habe ich den Startpunkt nochmals um den Betrag, der zuletzt bei der Uhr gemessen wurde, verschoben.
# Nun haben wir eine annähernde Angleichung von berechnetem Meßpunkt und dem momentanen Vor/Nachgang der Testuhr 
connection=sqlite3.connect(conftext)
pntr=connection.cursor()
pntr.execute("SELECT timedelta FROM muehle ORDER BY date DESC, time DESC LIMIT 1;")
compensationTime=pntr.fetchall()
connection.close()
compensationTime=compensationTime[0][0] # fetchall gibt ein Tupel (nur index 0 belegt?!) in einer Liste zurück e.g. [(wert, )]
if args.nocompensation:
  compensationTime=0

# die Funktion ohne Integerargument berechnet eine Zeit in der Zukunft, auf volle 5 Sek. teilbar
# und diese Zeit liegt 10 bis 15 Sekunden vor der Systemzeit des Computers
# die Funktion mit Integerargument berechnet eine Zeit in der Zukunft, auf volle 5 Sek. teilbar
# und diese Zeit liegt ungefähr 10 bis 15 Sekunden vor der Zeit der Testuhr. Als Argument dient in 
# diesem Fall der Messwert des zuletzt gemessenen Vor/Nachgangs als Integer.
newTimeMeasurePoint=gt10sekInFuture(compensationTime)

# wir rechnen hier mit der Unix-Zeit. Zeit des Programmstarts minus
# den gemessenen Wert (.timestamp = UNIX TIME)
unixtime_time_goal=strToTimestamp(newTimeMeasurePoint) # Das ist die Zeit der Testuhr bei
# der wir eine Messung auslösen

satisfied=False
while not satisfied:

  keyPressed=input('Drücken Sie die Eingabetaste exakt um %s Uhr ...' % newTimeMeasurePoint)
  # es wurde gedrueckt und wir halten die aktuelle Zeit nach PTB / Systemzeit fest
  unixtime_now=datetime.now().timestamp()
  diff=unixtime_time_goal-unixtime_now

  saveit=['y', 'Y', 'Yes', 'YES', 'yes', 'j', 'J', 'Ja', 'ja']
  repeatit=['a', 'A', 'again', 'Again', 'n', 'N', 'nein', 'Nein', 'no', 'No', 'NEIN', 'NO']
  finishit=['q', 'Q', 'Quit', 'quit', 'QUIT']

  print('Abweichung zur Referenzzeit: %.1f Sekunden.' % diff)
  question=input('Ergebnis in Datenbank speichern? ([y]es / [a]gain / [q]uit): ')
  if question in saveit:
    break

  if question in repeatit:
    print()
    newTimeGoal=gt10sekInFuture(compensationTime)
    newTimeMeasurePoint=newTimeGoal
    unixtime_time_goal=strToTimestamp(newTimeGoal)
    
  if question in finishit:
    sys.exit(0)

subprocess.run(['./mtm.sh', '-x %.1f' % diff], check=True)
