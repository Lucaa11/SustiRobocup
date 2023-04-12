import cv2
from RPi import GPIO
import numpy as np
import subprocess
import multiprocessing
import smbus
from smbus import SMBus
from threading import Event


bus = SMBus(1)
arduino=0x10
croce=0x36
piastra=0x34

cam = cv2.VideoCapture(-1)
exposuretime = 300 #va da 78 a 1250
command = "v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=" + str(exposuretime)
output = subprocess.call(command, shell=True)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)



class Camera:
    def telecamera(self):
        while True:
            try:
                delay = 0.05
                ret, frame = cam.read()
                frame = frame[2:160, 80:480]
                #convertire da BGR a HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                #frame = frame[2:200, 3:600]
                #definisco il range di colori per il rosso in BGR
                #lower_red = np.array([170,50,50])
                #upper_red = np.array([180,255,255])
                # lower mask (0-10)
                lower_red = np.array([0,50,50])
                upper_red = np.array([10,255,255])
                maskr1 = cv2.inRange(hsv, lower_red, upper_red)

                # upper mask (170-180)
                lower_red = np.array([170,50,50])
                upper_red = np.array([180,255,255])
                maskr2 = cv2.inRange(hsv, lower_red, upper_red)
                
                maskr = maskr1+maskr2
                contours, hierarchy = cv2.findContours(maskr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) != 0:
                    cnt = max(contours, key=cv2.contourArea)
                    area = cv2.contourArea(cnt)
                    if (area > 10000):
                        bus.write_byte(arduino,croce)
                        #sleep(0.05)
                        bus.write_byte(arduino,0x04)
                        print('trovato croce')
                    else:
                        print('no croce')
                else:
                    print('no croce')
                
                
                
                #blur = cv2.GaussianBlur(frame,(5,5),0)
                #definisco il range di colori per il nero in BGR
                lower_black = np.array([0, 0, 0])
                upper_black = np.array([180, 180, 190])
                # fa il mascheramento converte tramite hsv da BGR a HSV
                #maskr = cv2.inRange(hsv, lower_red, upper_red)
                # join my masks
                
                maskb = cv2.inRange(hsv, lower_black, upper_black)
                #blur1 = cv2.GaussianBlur(frame,(1,1),0)
                                    
                contours1, hierarchy1 = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours1) != 0:
                    cnt1 = max(contours1, key=cv2.contourArea)
                    area1 = cv2.contourArea(cnt1)
                    if (area1 > 20000):
                        #no i2c, pin normale, arduino riceve interrupt
                        #GPIO.output(20, GPIO.HIGH)
                        #Event().wait(delay)        
                        #GPIO.output(20, GPIO.LOW)
                        bus.write_byte(arduino,0x02)
                        bus.write_byte(arduino,piastra)
                        bus.write_byte(arduino,0x04)
                        print('trovato nero')
                        print(area1)
                    else:
                        print('no nero')
                        print(area1)
                else:
                    print('no nero')
                #mostra sia il mascheramento che il video
                cv2.imshow('video',frame)
                cv2.imshow('mascheramento rosso',maskr)
                cv2.imshow('mascheramento nero',maskb)
                
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                pass
        cam.release()
        cv2.destroyAllWindows()
            
        