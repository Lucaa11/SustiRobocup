import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)  
  
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
  
 
def my_callback(channel):  
    print ('ricevuto')
    i++
GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback, bouncetime=300)
while True:
    time.sleep(0.5)