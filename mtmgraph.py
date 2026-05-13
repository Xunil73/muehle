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


