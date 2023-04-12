import cv2
import numpy as np
import subprocess
import multiprocessing
#from multiprocessing import *
import libL
from libL import VL6180Xs
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
raddrizzamento_sinistra = 0x52
raddrizzamento_destra = 0x54

#LASER
sens1 = 0x11
sens2 = 0x12
sens3 = 0x13
sens4 = 0x14
sens5 = 0x15

#LASER
sensors=VL6180Xs(numSens=5)
for sensor in sensors.tof_sensor:
    if sensor.idModel != 0xB4:
        print("Not a valid sensor id: %X" % sensor.idModel)
    else:
        sensor.default_settings()
        

#GIROSCOPIO
gyro=BNO055()
if gyro.begin() is not True:
    print("Error initializing device")
    exit()

#INTERRUPT
a=0
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #cambiare pin
def my_callback(channel):  
    print ('ricevuto')
    a+=1
GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback, bouncetime=300)#rising edge


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
    

def raddrizzamento(lsDX1,lsDX2):
    if

def movimento():
    
    muro=120
    laser1 = 0
    laser2 = 0
    laser3 = 0
    laser4 = 0
    laser5 = 0
    
    while True:
        if a==1:
            a=0
            sleep(0.5)
            c = 0
            #while True:
            lsAV=sensors.tof_sensor[0].get_distance()
            lsDX1=sensors.tof_sensor[1].get_distance()
            lsDX2=sensors.tof_sensor[2].get_distance()
            lsSX1=sensors.tof_sensor[3].get_distance()
            lsSX2=sensors.tof_sensor[4].get_distance()
            print('laser_avanti = ',lsAV)
            print('laser1_sinistra = ',lsSX1)
            print('laser2_sinistra = ',lsSX2)
            print('laser1_destra = ',lsDX1)
            print('laser2_destra = ',lsDX2)
            print('--------------------------------------')
            sleep(1)
            
            #controllo
            if (( lsSX1 < muro) and (lsSX2 < muro)):
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
            if(( lsDX1 < muro )and (lsDX2 < muro)):
                laser3 = 1
            else:
                laser3 = 0
            
            
            
            
            if(laser3 == 0):
                destra()
                sleep(4)
                #continue
            elif (laser2 == 0):
                bus.write_byte(arduino,avanti)
                sleep(0.5)
                bus.write_byte(arduino, fermo)
                sleep(3.5)
                #continue
            elif(laser1 == 0):
                sinistra()
                sleep(4)
                #continue
            else:
                destra_x2()
                destra_x2()
                sleep(3)
                #continue
        else:
            sleep(0.5)
            
        
        
def camera():
    telecamera = Camera()
    telecamera.telecamera()
    

    

p1 = multiprocessing.Process(target = movimento)
p2 = multiprocessing.Process(target = camera)


p1.start()
p2.start()


p1.join()
p2.join()
