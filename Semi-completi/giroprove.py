import cv2
import numpy as np
import subprocess
from multiprocessing import *
import sys
from stl import VL6180Xs
from time import sleep
import busio
import smbus
from smbus import SMBus
import time
import RPi.GPIO as gpio
from libg import BNO055
from Prova_telecameara import Camera

bus = SMBus (1)
arduino=0x10

giroad = 0x26 
giroas = 0x27
fermo = 0x04
inv_destra = 0x03
inv_sinistra = 0x01
rallenta_destra = 0x28
rallenta_sinistra = 0x29
avanti = 0x02

#LASER
sens1 = 0x11
sens2 = 0x12
sens3 = 0x13
muro=200


laser1 = 0
laser2 = 0
laser3 = 0
#LASER
sensors=VL6180Xs(numSens=3)
for sensor in sensors.tof_sensor:
    if sensor.idModel != 0xB4:
        print("Not a valid sensor id: %X" % sensor.idModel)
    else:
        sensor.default_settings()
        
        
gyro=BNO055()
if gyro.begin() is not True:
    print("Error initializing device")
    exit()



def destra():
    gyro.begin()
    gradi = gyro.readAngle()
    bus.write_byte(arduino,giroad)
    while (gradi < 78) or (358 <= gradi <= 360) or (gradi<1) or (gradi>361):
        gradi = gyro.readAngle()
        if(48 < gradi < 52):
            bus.write_byte(arduino, rallenta_destra)
        #print(gradi)
    bus.write_byte(arduino, inv_destra)
    sleep(0.1)
    bus.write_byte(arduino, fermo)
    sleep(0.5)
    print("girato a destra")
    bus.write_byte(arduino,avanti)
    sleep(0.2)
    bus.write_byte(arduino, fermo)
    
    
def destra_x2():
    gyro.begin()
    gradi = gyro.readAngle()
    bus.write_byte(arduino,giroad)
    while (gradi < 81.5) or (358 <= gradi <= 360) or (gradi<1) or (gradi>361):
        gradi = gyro.readAngle()
        if(48 < gradi < 52):
            bus.write_byte(arduino, rallenta_destra)
        #print(gradi)
    bus.write_byte(arduino, inv_destra)
    sleep(0.1)
    bus.write_byte(arduino, fermo)
    sleep(0.5)
    print("girato a destra")
    sleep(1)
    #bus.write_byte(arduino,ava
    
    
def sinistra():
    gyro.begin()
    gradi = gyro.readAngle()
    bus.write_byte(arduino,giroas)
    while (gradi > 270) or (0 <= gradi <= 10) or (gradi<1) or (gradi>361):
        gradi = gyro.readAngle()
        if(298 < gradi < 302):
            bus.write_byte(arduino, rallenta_sinistra)
        #print(gradi)
    bus.write_byte(arduino, inv_sinistra)
    sleep(0.1)
    bus.write_byte(arduino, fermo)
    sleep(0.5)
    print("girato a sinistra")
    bus.write_byte(arduino,avanti)
    sleep(0.2)
    bus.write_byte(arduino, fermo)
    
    
    
c = 0
while True:
    lsAV=sensors.tof_sensor[0].get_distance()
    lsDX=sensors.tof_sensor[1].get_distance()
    lsSX=sensors.tof_sensor[2].get_distance()
    print('lsa',lsAV)
    print('lss',lsSX)
    print('lsd',lsDX)
    sleep(0.1)
    
    #controllo
    if ( lsSX < muro):
        laser1 = 1
    else:
        laser1 = 0
    if( lsAV < muro  ):
        c += 1
        if(c == 1):
            sleep(1)
            lsAV=sensors.tof_sensor[0].get_distance()
            print('lsa',lsAV)
        else:
            laser2 = 1
    else:
        laser2 = 0
    if( lsDX < muro ):
        laser3 = 1
    else:
        laser3 = 0
    
    
    
    
    if(laser2==1):
        if(laser3==0):
            destra()
            sleep(4)
            continue
        elif(laser1==0):
            sinistra()
            sleep(4)
            continue
        else:
            destra_x2()
            destra_x2()
            sleep(4)
            continue
            
            
    else:
        if(laser3==0):
           destra()
           sleep(4)
           continue
        elif(laser1 == 0):
           sinistra()
           sleep(4)
           continue
        else:
            bus.write_byte(arduino,avanti)
            sleep(0.2)
            bus.write_byte(arduino, fermo)
            print("Avanti")
            sleep(4)
            continue
    
            