import laser
import busio
import smbus
from smbus import SMBus
import time
import RPi.GPIO as gpio

ls = [0, 0, 0]

laser.init()
while True:
    ls = laser.read()
    print (ls[0])
