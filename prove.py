import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
angoli = [0, 0, 0]

while True:
    # angoli è l'array di 3 valori
     angoli = sensor.euler
     print(angoli[0])
     time.sleep(1)
   
   # inserendeo angoli[0] prende il primo valore
    #print(angoli[0])
