#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# Figure erzeugen
fig, ax = plt.subplots(figsize=(8, 4))

# Linie zeichnen
ax.plot(x, y, marker="o")

# Y-Achse von -50 bis +50
ax.set_ylim(-50, 50)

# Gitter einschalten
ax.grid(True)

# X-Achse: 1 Hauptgitter pro Tag
ax.xaxis.set_major_locator(mdates.DayLocator())

# Datumsformat
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))

# Beschriftung drehen
plt.xticks(rotation=45)

# Layout optimieren
plt.tight_layout()

# Anzeigen
plt.show()

