#!/usr/bin/env python3

from time import time
from datetime import datetime, timedelta

# diese Funktion nimmt die aktuelle Zeit und
# rechnet Sekunden bis zu den nächsten vollen 
# fuenf Sekunden dazu und anschliessend nochmals
# plus zehn Sekunden. Gibt die errechnete Uhrzeit
# als normalen String zurück.
# Beispiel: es ist 14:30 und 43 Sekunden. Die errechnete
# Uhrzeit ist dann 14:30 und 55 Sekunden 
# 43 Sek + 2 = 45 -> 45 + 10 = 55
def gt10sekInFuture(compensation=0):
  comp=timedelta(seconds=compensation)
  jetzt=datetime.today() + comp
  diffZuFuenf=int(jetzt.strftime('%S')) % 5
  diffZuFuenf=5-diffZuFuenf
  ziel=jetzt + timedelta(seconds=diffZuFuenf + 10)
  return datetime.strftime(ziel, '%H:%M:%S')




