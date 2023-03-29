import cv2
import numpy as np
import subprocess
import multiprocessing
from classecroce import camera
from Prova_telecameara import Camera



#telecamera = Camera()
#telecamera.telecamera()

def camera():
    telecamera = Camera()
    telecamera.telecamera()
    

    

#p1 = multiprocessing.Process(target = movimento)
p2 = multiprocessing.Process(target = camera)


#p1.start()
p2.start()


#p1.join()
p2.join()