import cv2
import numpy as np
import subprocess
import multiprocessing
import smbus
from smbus import SMBus


bus = SMBus (1)
arduino=0x10
croce=0x36
piastra=0x34

class camera:
    def __init__(self,cam):
        
        self.cam=cam
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #self.cam.set(cv2.CAP_PROP_EXPOSURE, -4)

        
        #exposuretime = 100#va da 78 a 1250
        #command = "v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=" + str(exposuretime)
        #output = subprocess.call(command, shell=True)
        
        self.res=' '
        
        #definisco il range di colori per il rosso in BGR
        self.lower_red = np.array([159, 50, 70])
        self.upper_red = np.array([180, 255, 255 ])
        
        #definisco il range di colori per il nero in BGR
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([205, 85, 76])
    
    def run(self,res):
        while True:
            try:
                self.ret, self.frame =self.cam.read()
                
                #convertire da BGR a HSV
                self.frame = self.frame[0:400,300:1100]
                self.frame = cv2.resize(self.frame, (320, 240), interpolation= cv2.INTER_LINEAR)
                hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                
                # fa il mascheramento converte tramite hsv da BGR a HSV
                self.maskr = cv2.inRange(hsv, self.lower_red, self.upper_red)
                self.maskb = cv2.inRange(hsv, self.lower_black, self.upper_black)
                
                contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                  
                #mostra sia il mascheramento che il video
                cv2.imshow('video',self.frame)
                cv2.imshow('mascheramento rosso',self.maskr)
                cv2.imshow('mascheramento nero',self.maskb)
                
            except:
                   pass
    #va inserito in ogni programma

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #cam.release()
    #cv2.destroyAllWindows()
        
#if __name__ == '__main__':
#    cam =  cv2.VideoCapture(0)
#    telecamera = camera(cam)
#    telecamera.run('a')
#    cam.release()
#    cv2.destroyAllWindows()