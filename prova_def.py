import sys
from stl import VL6180Xs
from time import sleep
import busio
import smbus
from smbus import SMBus
import time
import RPi.GPIO as gpio
from giros import BNO055

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


#BNO
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
        if (giro > 85 and giro < 95):
            bus.write_byte(arduino,giroad)
            print('girato a destra')
            rst()
        
    
    if (lsDX < 80 and lsAV < 80):
        print('c è il muro a destra e avanti svolta a sinistra')
        time.sleep(0.5)
        bus.write_byte(arduino,0x15)
        if (giro > 265 and giro < 276.5):
            bus.write_byte(arduino,giroas)
            print('girato')
            rst()
        
    if (lsSX < 80 and lsAV < 80):
        print('c è il muro a sinistra e avanti svolta a destra')
        time.sleep(0.5)
        bus.write_byte(arduino,0x16)
        if (giro > 85 and giro < 95):
            bus.write_byte(arduino,giroad)
            print('girato a destra')
            rst()
            
    if(lsDX < 80):
        print('destra occupata vai avanti')
        time.sleep(0.5)
        bus.write_byte(arduino,0x17)
        
    if(lsSX < 80):
        print('sinistra occupato vai a destra')
        time.sleep(0.5)
        bus.write_byte(arduino,0x18)
        if (giro > 85 and giro < 95):
            bus.write_byte(arduino,giroad)
            print('girato a destra')
            rst()
        
    
        
        
        
   