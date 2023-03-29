import sys
from stl import VL6180Xs
from time import sleep
import busio
import smbus
from smbus import SMBus
import time
import RPi.GPIO as gpio
from giros import BNO055
import cv2
import numpy as np
import subprocess
from multiprocessing import *
from classecroce import camera

#I2C
bus = SMBus (1)
arduino=0x10

#LASER
sens1 = 0x11
sens2 = 0x12
sens3 = 0x13
#LASER
sensors=VL6180Xs(numSens=3)
for sensor in sensors.tof_sensor:
    if sensor.idModel != 0xB4:
        print("Not a valid sensor id: %X" % sensor.idModel)
    else:
        sensor.default_settings()

#TELECAMERA
#cam =  cv2.VideoCapture(0)
#telecamera = camera(cam)
#[telecamera.run('a')
#cam.release()
#cv2.destroyAllWindows()


#BNO
giroad = 0x26 
giroas = 0x27

gyro=BNO055()
if gyro.begin() is not True:
    print("Error initializing device")
    exit()
gyro.setExternalCrystalUse(True)
    
#Resetta il BNO
def rst():
    gyro.setMode(BNO055.OPERATION_MODE_CONFIG)
    gyro.writeBytes(BNO055.BNO055_SYS_TRIGGER_ADDR, [0x20])
    time.sleep(0.5)
    gyro.writeBytes(BNO055.BNO055_PWR_MODE_ADDR, [BNO055.POWER_MODE_NORMAL])
    while gyro.readBytes(BNO055.BNO055_CHIP_ID_ADDR)[0] != BNO055.BNO055_ID:
        time.sleep(0.01)
    time.sleep(0.05)
    gyro.writeBytes(BNO055.BNO055_PWR_MODE_ADDR, [BNO055.POWER_MODE_NORMAL])
    time.sleep(0.01)
    gyro.writeBytes(BNO055.BNO055_PAGE_ID_ADDR, [0])
    gyro.writeBytes(BNO055.BNO055_SYS_TRIGGER_ADDR, [0])
    time.sleep(0.01)
    gyro.setMode(BNO055.OPERATION_MODE_NDOF)
    time.sleep(0.02)

while True:
    giro = gyro.getVector(BNO055.VECTOR_EULER)[0]
    print(giro)
    
    lsAV=sensors.tof_sensor[0].get_distance()
    lsDX=sensors.tof_sensor[1].get_distance()
    lsSX=sensors.tof_sensor[2].get_distance()
    
    if(lsDX > 180 and lsSX > 180 and lsAV > 180):
        print('tutte le strade libere')
        time.sleep(0.5)
        bus.write_byte(arduino,0x14)
        while (giro < 88.5):
            giro = gyro.getVector(BNO055.VECTOR_EULER)[0]
            print('Sto girando') 
        bus.write_byte(arduino,giroad)
        print('girato a destra')
        time.sleep(0.5)
        #rst()
        bus.write_byte(arduino,0x17)
    elif(lsDX < 80 and lsAV < 80):
        print('c è il muro a destra e avanti svolta a sinistra')
        time.sleep(0.5)
        bus.write_byte(arduino,0x15)
        while (giro > 271.5):
            giro = gyro.getVector(BNO055.VECTOR_EULER)[0]
            print('Sto girando')
        bus.write_byte(arduino,giroas)
        print('girato')
        #rst()
        bus.write_byte(arduino,0x17)
    elif(lsSX < 80 and lsAV < 80):
        print('c è il muro a destra e avanti svolta a sinistra')
        time.sleep(0.5)
        bus.write_byte(arduino,0x15)
        while (giro > 271.5):
            giro = gyro.getVector(BNO055.VECTOR_EULER)[0]
            print('Sto girando')
        bus.write_byte(arduino,giroas)
        print('girato')
        #rst()
        bus.write_byte(arduino,0x17)
    elif(lsDX < 80):
        print('destra occupata vai avanti')
        time.sleep(0.5)
        bus.write_byte(arduino,0x17)
    else:
        print('destra libera')
        time.sleep(0.5)
        bus.write_byte(arduino,0x14)
        while (giro > 271.5):
            giro = gyro.getVector(BNO055.VECTOR_EULER)[0]
            print('Sto girando')
        bus.write_byte(arduino,giroas)
        print('girato')
        #rst()
        bus.write_byte(arduino,0x17)
