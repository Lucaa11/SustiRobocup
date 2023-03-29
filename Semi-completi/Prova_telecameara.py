import cv2
import numpy as np
import subprocess
import multiprocessing
import smbus
from smbus import SMBus


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
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([205, 85, 76])
            # fa il mascheramento converte tramite hsv da BGR a HSV
            maskr = cv2.inRange(hsv, lower_red, upper_red)
            maskb = cv2.inRange(hsv, lower_black, upper_black)
            #mostra sia il mascheramento che il video
            cv2.imshow('video',frame)
            cv2.imshow('mascheramento rosso',maskr)
            cv2.imshow('mascheramento nero',maskb)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
            
        