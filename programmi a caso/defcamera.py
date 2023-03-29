import cv2
import numpy as np
import subprocess
from multiprocessing import *
from classecroce import camera

cam =  cv2.VideoCapture(0)
telecamera = camera(cam)
telecamera.run('a')
cam.release()
cv2.destroyAllWindows()
