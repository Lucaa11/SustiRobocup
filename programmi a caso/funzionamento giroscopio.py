from giro import*
import RPi.GPIO as gpio
import board
import busio
import time
from multiprocessing import Queue
import smbus
from smbus import SMBus



gr = Queue() #inizializzazione
par = IlMioThread(gr)
par.start()
bus = SMBus (1)
arduino=0x10
giro=0x27
giro_RST = [4]
while True:
    giro = gr.get()[0]
    print(giro)
    
    if (giro > 30):
        print('??')
    