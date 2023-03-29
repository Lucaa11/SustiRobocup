import laseri
import RPi.GPIO as gpio
import board
import busio
import math
import time


laser_MM = [0, 0, 0]

# serial = Serial.SerialeATmega()
laser = laseri.Laser()

# gpio.setup(led[0],gpio.OUT)
# gpio.setup(led[1],gpio.OUT)

while True:
#     letturaseriale = serial.read()
    try:
        laser_MM = laser.read()
        print('ls1 =',laser_MM[0])
    except:
        pass
   #print('laser 2 = ', laser_MM[1])
    #print('laser 3 = ', laser_MM[2])
    
    #ang_DX = (math.atan((laser_MM[1] - laser_MM[2])/170))*180/math.pi
    #ang_SX = (math.atan((laser_MM[4] - laser_MM[3])/170))*180/math.pi
    
    #print(str(ang_DX) + " | " + str(ang_SX))
#     print(letturaseriale)
#     
#     gpio.output(led[0],gpio.HIGH)
#     gpio.output(led[1],gpio.HIGH)
#     
#     time.sleep(0.5)
#     
#     gpio.output(led[0],gpio.LOW)
#     gpio.output(led[1],gpio.LOW)
#     
    time.sleep(0.01)