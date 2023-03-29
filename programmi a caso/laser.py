import RPi.GPIO as gpio
import board
import busio
import time
import adafruit_vl6180x as vl6180

laser_SHDN = [21,20,16]
laser_ADDRESS = [0x20,0x22,0x24]
laser_MM = [0, 0, 0]
I2C = busio.I2C(board.SCL, board.SDA)
ls = [0,0,0]   #creazione lista

def init():
    for i in range(0, 2):
        gpio.setup(laser_SHDN[i],gpio.OUT)
        gpio.output(laser_SHDN[i],gpio.LOW)
    
    for i in range(0, 2):
       
        try:
            gpio.output(laser_SHDN[i],gpio.HIGH)
            sensor = vl6180.VL6180X(I2C)
            sensor._write_8(0x212, laser_ADDRESS[i])
            time.sleep(0.01)
            ls.append([0])    #aggiungo elementi alla lista
        except:
            print ('errore laser')

def read():
    global var
    for i in range(0, 2):
        laser_MM = [0, 0, 0, 0, 0, 0, 0]
        for k in range(5):
            sensor = vl6180.VL6180X(I2C, address = laser_ADDRESS[i])
            laser_MM[i] += sensor.range
        laser_MM[i] = laser_MM[i]/5
        ls[i]= laser_MM[i]
        #print("Range: {0}mm".format(laser_MM[i]))
        
    time.sleep(1)