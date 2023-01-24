import board
import busio
import adafruit_bno055
import time

import threading
from multiprocessing import Queue
from random import randint

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
angoli = [0, 0, 0]

def read(Queue): 
    while True:
        # angoli è l'array di 3 valori
        angoli = sensor.euler
        Queue.put_nowait(angoli)
        # inserendeo angoli[0] prende il primo valore
        time.sleep(0.1)


class IlMioThread (threading.Thread):      # classe per 2 programmi in parallelo
   def __init__(self,Queue):
      threading.Thread.__init__(self)
      self.Queue = Queue
   def run(self):
        read(self.Queue)
# Creazione dei thread
#thread1 = IlMioThread("Thread#1", randint(1,100))