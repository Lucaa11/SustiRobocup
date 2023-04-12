import libL
from libL import VL6180Xs
from time import sleep
import busio
import smbus
from smbus import SMBus
import time
import RPi.GPIO as gpio

#LASER
sensors=VL6180Xs(numSens=5)
for sensor in sensors.tof_sensor:
    if sensor.idModel != 0xB4:
        print("Not a valid sensor id: %X" % sensor.idModel)
    else:
        sensor.default_settings()
        
while True:
    lsAV=sensors.tof_sensor[0].get_distance()
    lsDX1=sensors.tof_sensor[1].get_distance()
    lsDX2=sensors.tof_sensor[2].get_distance()
    lsSX1=sensors.tof_sensor[3].get_distance()
    lsSX2=sensors.tof_sensor[4].get_distance()
    print('lsa',lsAV)
    print('lssx1',lsSX1)
    print('lssx2',lsSX2)
    print('lsdx1',lsDX1)
    print('lsdx2',lsDX2)
    print('--------------------------------------')
    sleep(1)q