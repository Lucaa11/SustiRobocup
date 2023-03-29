import cv2
import numpy as np
import subprocess

cam = cv2.VideoCapture(-1)
exposuretime = 300 #va da 78 a 1250

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
command = "v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=" + str(exposuretime)
output = subprocess.call(command, shell=True)

while True:
    try:
        ret, frame = cam.read()
        
        #convertire da BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #definisco il range di colori per il rosso in BGR
        lower_red = np.array([159, 50, 70])
        upper_red = np.array([180, 255, 255 ])
        blur = cv2.GaussianBlur(frame,(5,5),0)
        # fa il mascheramento converte tramite hsv da BGR a HSV
        maskr = cv2.inRange(hsv, lower_red, upper_red)
        
        contours, hierarchy = cv2.findContours(maskr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
             cnt = max(contours, key=cv2.contourArea)
             area = cv2.contourArea(cnt)
             if (area > 35000):
                 print('trovato')
        
             else:
                 print('no croce')
        else:
            print('no croce')
            
        #mostra sia il mascheramento che il video
        cv2.imshow('video',frame)
        cv2.imshow('mascheramento rosso',maskr)
    except:
        pass
   
    #va inserito in ogni programma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()