from giros import BNO055
import time
import smbus
from smbus import SMBus

bus = SMBus (1)
arduino=0x10
giro=0x27

#Resetta il BNO
def rst():
    gyro.setMode(BNO055.OPERATION_MODE_CONFIG)
    gyro.writeBytes(BNO055.BNO055_SYS_TRIGGER_ADDR, [0x20])
    time.sleep(0.5)
    gyro.writeBytes(BNO055.BNO055_PWR_MODE_ADDR, [BNO055.POWER_MODE_NORMAL])
    while gyro.readBytes(BNO055.BNO055_CHIP_ID_ADDR)[0] != BNO055.BNO055_ID:
        time.sleep(0.01)

def acc():
    time.sleep(0.05)
    gyro.writeBytes(BNO055.BNO055_PWR_MODE_ADDR, [BNO055.POWER_MODE_NORMAL])
    time.sleep(0.01)
    gyro.writeBytes(BNO055.BNO055_PAGE_ID_ADDR, [0])
    time.sleep(0.01)
    gyro.setMode(BNO055.OPERATION_MODE_NDOF)
    time.sleep(0.02)
    
gyro=BNO055()
if gyro.begin() is not True:
    print("Error initializing device")
    exit()
gyro.setExternalCrystalUse(True)
while True:
    try:
        a = gyro.getVector(BNO055.VECTOR_EULER)[0]
        print(a)
    
        if (a > 265 and a < 276.5):
            #bus.write_byte(arduino,giro)
            print('ok')
            rst()
            acc()
        time.sleep(0.5)
            #bus.write_byte(arduino,0x01)
    except:
        pass
    
        
   
        

