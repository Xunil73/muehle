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
  daten.append((f"{dat} {tme}", delta))

# Datum/Zeit umwandeln
x = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, y in daten]
y = [y for d, y in daten]

fig, ax = plt.subplots(figsize=(12, 4))

# Plot
ax.plot(x, y, marker="o")

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
