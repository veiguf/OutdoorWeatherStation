#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "22jj" # Change XYZ to the UID of your Outdoor Weather Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather

from datetime import datetime
import csv

file = open("OutdoorWeatherStationData.csv", "w", encoding="utf-8")
with file:
    writer = csv.writer(file)
    writer.writerow(["DateTime", "Temperature [°C]", "Humidity [%RH]", "Wind Speed [m/s]", "Gust Speed [m/s]", "Rain [mm]", "Wind Direction"])

# Callback function for station data callback
def cb_station_data(identifier, temperature, humidity, wind_speed, gust_speed, rain,
                    wind_direction, battery_low):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time:", current_time)
    print("Identifier (Station): " + str(identifier))
    print("Temperature (Station): " + str(temperature/10.0) + " °C")
    print("Humidity (Station): " + str(humidity) + " %RH")
    print("Wind Speed (Station): " + str(wind_speed/10.0) + " m/s")
    print("Gust Speed (Station): " + str(gust_speed/10.0) + " m/s")
    print("Rain (Station): " + str(rain/10.0) + " mm")

    if wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_N:
        print("Wind Direction (Station): N")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NNE:
        print("Wind Direction (Station): NNE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NE:
        print("Wind Direction (Station): NE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ENE:
        print("Wind Direction (Station): ENE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_E:
        print("Wind Direction (Station): E")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ESE:
        print("Wind Direction (Station): ESE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SE:
        print("Wind Direction (Station): SE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SSE:
        print("Wind Direction (Station): SSE")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_S:
        print("Wind Direction (Station): S")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SSW:
        print("Wind Direction (Station): SSW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_SW:
        print("Wind Direction (Station): SW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_WSW:
        print("Wind Direction (Station): WSW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_W:
        print("Wind Direction (Station): W")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_WNW:
        print("Wind Direction (Station): WNW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NW:
        print("Wind Direction (Station): NW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_NNW:
        print("Wind Direction (Station): NNW")
    elif wind_direction == BrickletOutdoorWeather.WIND_DIRECTION_ERROR:
        print("Wind Direction (Station): Error")

    print("Battery Low (Station): " + str(battery_low))
    print("")

    file = open("OutdoorWeatherStationData.csv", "a", encoding="utf-8")
    with file:
        writer = csv.writer(file)
        writer.writerow([current_time, temperature/10.0, humidity, wind_speed/10.0, gust_speed/10.0, rain/10.0, wind_direction])

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
