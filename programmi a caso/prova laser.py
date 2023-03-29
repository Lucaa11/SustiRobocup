import laser
import RPi.GPIO as gpio
import board
import busio
import smbus
from smbus import SMBus
import time

bus = SMBus (1)
arduino = 0x10
sens0 = 0x11

laser.init()
#[1 = DAVANTI] [2 = DESTRA] [3 = SINISTRA]
while True:
    laser.read()
    print('laser1 :', laser.ls[0])
    print('laser2 :', laser.ls[1])
    #print('laser3 :', laser.ls[2])
    #LASER DAVANTI
    #laser.ls[0]
    #LASER DESTRA
    #laser.ls[1]
    #LASER SINISTRA
    #laser.ls[2]
    
        

    
