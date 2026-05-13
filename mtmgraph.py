#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import subprocess

result = subprocess.run(["./mtm.sh", "-r"], capture_output=True, text=True)
output = result.stdout

daten=[]
for ele in output.splitlines():
  nr, dat, tme, delta, vor = ele.split()
  #print(dat, tme, delta)
  daten.append((f"{dat} {tme}", delta))




# Datum/Zeit umwandeln
x = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, y in daten]
y = [y for d, y in daten]

# Anzahl Tage bestimmen
anzahl_tage = (max(x) - min(x)).days + 1

# 2 cm pro Tag
breite_cm = anzahl_tage * 2

# cm → inch
breite_inch = breite_cm / 2.54

# Figure erzeugen
fig, ax = plt.subplots(figsize=(breite_inch, 5))

# Plot
ax.plot(x, y)

# Datumsformat
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))

# automatische Datums-Ticks
#fig.autofmt_xdate()

# Datumsbeschrifung drehen
plt.xticks(rotation=45)

plt.plot(x, y)

plt.show()
