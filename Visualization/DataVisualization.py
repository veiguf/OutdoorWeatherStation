#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

data_file = "/home/veit/Dokumente/OutdoorWeatherStation/SensorData.csv"

with open(data_file) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    data = []
    for row in reader:
        data.append(row)

now = datetime.now()
now = datetime(2023,10,31,23,59,59,999999)

array = np.array(data)

TCheck = np.array(array[:, 0], dtype="datetime64")

tDelta = timedelta(seconds=10)
tMin = datetime(now.year,now.month,1)

keep = []
for i in range(len(TCheck)-1):
    if TCheck[i] >= tMin and TCheck[i] <= now:
        if i == 0:
            keep.append(i)
        elif (TCheck[i]-TCheck[i-1]) > tDelta:
            keep.append(i)

DateTime = np.array(array[keep, 0], dtype="datetime64")
Temperature = np.array(array[keep, 1], dtype="float")
Humidity = np.array(array[keep, 2], dtype="int")
WindSpeed = np.array(array[keep, 3], dtype="float")
GustSpeed = np.array(array[keep, 4], dtype="float")
WindDirection = np.array(array[keep, 5], dtype="str")
Rain = np.array(array[keep, 6], dtype="float")
BatteryStatus = np.array(array[keep, 7], dtype="str")

plt.figure()
plt.plot(DateTime, Temperature, color="C0")
plt.ylabel(header[1])
plt.xlim(DateTime[0], DateTime[-1])
plt.xticks(rotation=45, ha='right')
plt.title(now.strftime("%B %Y"))
plt.grid()
plt.tight_layout()
plt.savefig(now.strftime("%Y-%m")+"_Temp.svg")

plt.figure()
plt.plot(DateTime, Humidity, color="C1")
plt.ylabel(header[2])
plt.xlim(DateTime[0], DateTime[-1])
plt.ylim(0, 100)
plt.xticks(rotation=45, ha='right')
plt.title(now.strftime("%B %Y"))
plt.grid()
plt.tight_layout()
plt.savefig(now.strftime("%Y-%m")+"_Hum.svg")

plt.figure()
plt.plot(DateTime, Rain, color="C4")
plt.ylabel(header[6])
plt.xlim(DateTime[0], DateTime[-1])
plt.xticks(rotation=45, ha='right')
plt.title(now.strftime("%B %Y"))
plt.grid()
plt.tight_layout()
plt.savefig(now.strftime("%Y-%m")+"_Rain.svg")

plt.figure()
plt.hist(WindSpeed, bins=range(int(WindSpeed.max()+1)+1), density=True, color="C2")
plt.xlabel(header[3])
plt.ylabel("Relative Frequency")
plt.title(now.strftime("%B %Y"))
plt.tight_layout()
plt.savefig(now.strftime("%Y-%m")+"_WindSpeed.svg")

plt.figure()
plt.hist(GustSpeed, bins=range(int(GustSpeed.max()+1)+1), density=True, color="C3")
plt.xlabel(header[4])
plt.ylabel("Relative Frequency")
plt.title(now.strftime("%B %Y"))
plt.tight_layout()
plt.savefig(now.strftime("%Y-%m")+"_GustSpeed.svg")
