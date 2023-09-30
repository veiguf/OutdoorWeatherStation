#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "22jj" # Change XYZ to the UID of your Outdoor Weather Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather

from datetime import datetime
import csv
import os.path

data_file = "/home/veit/Dokumente/OutdoorWeatherStation/SensorData.csv"

if os.path.isfile(data_file) == False:
    file = open(data_file, "w", encoding="utf-8")
    with file:
        writer = csv.writer(file)
        writer.writerow(["Date and Time", "Temperature [°C]", "Humidity [%RH]", "Wind Speed [m/s]", "Gust Speed [m/s]", "Wind Direction", "Rain [mm]", "Battery Status"])

# Callback function for station data callback
def cb_station_data(identifier, temperature, humidity, wind_speed, gust_speed, rain,
                    wind_direction, battery_low):

    now = datetime.now()

    if wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_N:
        wind_direction_str = "N"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NNE:
        wind_direction_str = "NNE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NE:
        wind_direction_str = "NE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ENE:
        wind_direction_str = "ENE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_E:
        wind_direction_str = "E"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ESE:
        wind_direction_str = "ESE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SE:
        wind_direction_str = "SE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SSE:
        wind_direction_str = "SSE"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_S:
        wind_direction_str = "S"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SSW:
        wind_direction_str = "SSW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SW:
        wind_direction_str = "SW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_WSW:
        wind_direction_str = "WSW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_W:
        wind_direction_str = "W"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_WNW:
        wind_direction_str = "WNW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NW:
        wind_direction_str = "NW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NNW:
        wind_direction_str = "NNW"
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ERROR:
        wind_direction_str = "Error"

    if battery_low == False:
        battery_status = "OK"
    elif battery_low == True:
        battery_status = "LOW"
    else:
        battery_status = "???"

    # print("Current Date and Time:", now)
    # print("Identifier (Station): " + str(identifier))
    # print("Temperature (Station): " + str(temperature/10.0) + " °C")
    # print("Humidity (Station): " + str(humidity) + " %RH")
    # print("Wind Speed (Station): " + str(wind_speed/10.0) + " m/s")
    # print("Gust Speed (Station): " + str(gust_speed/10.0) + " m/s")
    # print("Rain (Station): " + str(rain/10.0) + " mm")
    # print("Wind Direction (Station): " + wind_direction_str)
    # print("Battery Status (Station): " + battery_status)
    # print("")

    file = open(data_file, "a", encoding="utf-8")
    with file:
        writer = csv.writer(file)
        writer.writerow([now, temperature/10.0, humidity, wind_speed/10.0, gust_speed/10.0, wind_direction_str, rain/10.0, battery_status])

# Callback function for sensor data callback
def cb_sensor_data(identifier, temperature, humidity):
    print("Identifier (Sensor): " + str(identifier))
    print("Temperature (Sensor): " + str(temperature/10.0) + " °C")
    print("Humidity (Sensor): " + str(humidity) + " %RH")
    print("")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    ow = BrickletOutdoorWeather(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Enable station data callbacks
    ow.set_station_callback_configuration(True)

    # Enable sensor data callbacks
    ow.set_sensor_callback_configuration(True)

    # Register station data callback to function cb_station_data
    ow.register_callback(ow.CALLBACK_STATION_DATA, cb_station_data)

    # Register sensor data callback to function cb_sensor_data
    ow.register_callback(ow.CALLBACK_SENSOR_DATA, cb_sensor_data)

    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()
