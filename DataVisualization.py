#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from git import Repo

data_file = "/home/veit/Dokumente/OutdoorWeatherStation/SensorData.csv"

with open(data_file) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    header[1]="Temperature [°C]"
    data = []
    for row in reader:
        data.append(row)

now = datetime.now()
# now = datetime(2024,7,31,23,59,59,999999)
# tMin = datetime(now.year,now.month,1)
tMin = datetime(2024,8,1)

tDelta = timedelta(seconds=10)


array = np.array(data)

TCheck = np.array(array[:, 0], dtype="datetime64")

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

fig, axs = plt.subplots(3, 1, sharex='col', figsize=(7,7))
fig.suptitle("Weather data: "+tMin.strftime("%B %Y")+" - "+now.strftime("%B %Y"))
axs[0].plot(DateTime, Temperature, ls="", marker=".", color="C0")
axs[0].set_ylabel(header[1])
axs[0].grid()
axs[1].plot(DateTime, Humidity, ls="", marker=".", color="C1")
axs[1].set_ylabel(header[2])
axs[1].set_ylim(0, 100)
axs[1].grid()
axs[2].plot(DateTime, Rain, ls="", marker=".", color="C4")
axs[2].set_ylabel(header[6])
axs[2].grid()
axs[2].set_xlim(DateTime[0], DateTime[-1])
axs[2].tick_params(axis='x', labelrotation=45)
plt.tight_layout()
plt.savefig("/home/veit/Dokumente/OutdoorWeatherStation/Visualization/"+tMin.strftime("%Y-%m")+"_THR.svg")

fig, axs = plt.subplots(1, 2, sharey='row', figsize=(7,3.5))
fig.suptitle("Wind speed histograms: "+tMin.strftime("%B %Y")+" - "+now.strftime("%B %Y"))
axs[0].hist(WindSpeed, bins=range(int(WindSpeed.max()+1)+1), density=True, color="C2")
axs[0].set_xlabel(header[3])
axs[0].set_ylabel("Relative Frequency")
axs[0].grid(axis='y')
axs[1].hist(GustSpeed, bins=range(int(GustSpeed.max()+1)+1), density=True, color="C3")
axs[1].set_xlabel(header[4])
axs[1].grid(axis='y')
plt.tight_layout()
plt.savefig("/home/veit/Dokumente/OutdoorWeatherStation/Visualization/"+tMin.strftime("%Y-%m")+"_Wind.svg")

repo = Repo('/home/veit/Dokumente/OutdoorWeatherStation')  # if repo is CWD just do '.'
repo.index.add(['Visualization'])
repo.index.commit(now.strftime("%Y-%m-%d %H:%M:%S.%f")+"-Visualization")
origin = repo.remote('origin')
origin.push()
