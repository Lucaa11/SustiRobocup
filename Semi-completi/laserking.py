import sys
from stl import VL6180Xs
from time import sleep
import RPi.GPIO as GPIO  # Import GPIO functions


sensors=VL6180Xs(numSens=3)
for sensor in sensors.tof_sensor:
    if sensor.idModel != 0xB4:
        print("Not a valid sensor id: %X" % sensor.idModel)
    else:
        sensor.default_settings()


"""-- MAIN LOOP --"""
while True:
    ls1=sensors.tof_sensor[0].get_distance()
    ls2=sensors.tof_sensor[1].get_distance()
    ls3=sensors.tof_sensor[2].get_distance()
    print(ls1)
    print(ls2)
    print(ls3)
        #print ("Distance measured by "+str(hex(sensor.get_register(0x0212)))+" is : %d mm" % sensor.get_distance())
    sleep(1)
    
    