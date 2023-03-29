import cv2
import numpy as np
import subprocess
import multiprocessing
import smbus
from smbus import SMBus

bus = SMBus (1)
arduino=0x10

cam =  cv2.VideoCapture(-1)
exposuretime = 300 #va da 78 a 1250
command = "v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=" + str(exposuretime)
output = subprocess.call(command, shell=True)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)


class Camera:
    def telecamera(self):
        while True:
            ret, frame = cam.read()
        
            #convertire da BGR a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            #definisco il range di colori per il rosso in BGR
            lower_red = np.array([159, 50, 70])
            upper_red = np.array([180, 255, 255 ])
            blur = cv2.GaussianBlur(frame,(5,5),0)
            #definisco il range di colori per il nero in BGR
            lower_black = np.array([15, 15, 15])
            upper_black = np.array([195, 195, 195])
            # fa il mascheramento converte tramite hsv da BGR a HSV
            maskr = cv2.inRange(hsv, lower_red, upper_red)
            maskb = cv2.inRange(hsv, lower_black, upper_black)
            contours, hierarchy = cv2.findContours(maskr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != 0:
            cnt = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(cnt)
            if (area > 35000):
                bus.write_byte(arduino, )#qualcosa
                print('trovato croce')
             else:
                print('no croce')
            else:
                print('no croce')
                
            contours1, hierarchy1 = cv2.findContours(maskb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours1) != 0:
            cnt1 = max(contours, key=cv2.contourArea)
            area1 = cv2.contourArea(cnt1)
            if (area > 30000):
                bus.write_byte(arduino, )#qualcosa
                print('trovato nero')
             else:
                print('no nero')
            else:
                print('no nero')
            #mostra sia il mascheramento che il video
            cv2.imshow('video',frame)
            cv2.imshow('mascheramento rosso',maskr)
            cv2.imshow('mascheramento nero',maskb)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
            
        