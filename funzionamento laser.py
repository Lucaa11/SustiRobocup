#from giroscopio import*
import laser
import RPi.GPIO as gpio
import board
import busio
import time
#from multiprocessing import Queue

laser.init()
laser.read() 
print(laser.ls)  #stampo la lista all'interno delle [] indico la posizione del sensore che mi interessa


'''gr = Queue() #inizializzazione
par = IlMioThread(gr)    
par.start()
    
while True:

    if gr.get()[0] > 0.1 and gr.get()[0] < 100:
        print(gr.get()[0],'dx')
        time.sleep(0.5)
    elif gr.get()[0] > 260 and gr.get()[0] < 359.9:
        print(gr.get()[0],'sx')
        time.sleep(0.5)'''
    

    
