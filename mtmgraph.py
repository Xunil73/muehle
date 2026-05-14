#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import subprocess

result = subprocess.run(["./mtm.sh", "-r"], capture_output=True, text=True)
output = result.stdout

daten=[]
for ele in output.splitlines():
  nr, dat, tme, delta, vor = ele.split()
  #print(dat, tme, delta)
  daten.append((f"{dat} {tme}", float(delta)))

# Datum/Zeit umwandeln
x = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, y in daten]
y = [y for d, y in daten]

#debug
for i, ele in enumerate(x):
  print(ele, y[i])

fig, ax = plt.subplots(figsize=(12, 5))

# Gitter einschalten
ax.grid(True,
        color="grey",
        which="major",
        linestyle="--",       # Strichart: '-', '--', '-.', ':'
        linewidth=0.8         # Dicke)
       )
# Plot
ax.plot(x, y, marker=".")

# wir setzen die Y-Achse
ax.set_ylim(min(y)-1, max(y)+1)
ax.set_yticks([-30,-25,-20,-15,-10,-5,0,5,10,15,20])

# ---------------------------------------------------
# Alle Tage zwischen min und max erzeugen
# ---------------------------------------------------
start = min(x).date()
ende  = max(x).date()

alle_tage = []
tag = start

while tag <= ende:
    alle_tage.append(datetime.combine(tag, datetime.min.time()))
    tag += timedelta(days=1)

# ---------------------------------------------------
# Diese Tage als X-Ticks setzen
# ---------------------------------------------------
ax.set_xticks(alle_tage)

# Datumsformat
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))

# Labels drehen
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
