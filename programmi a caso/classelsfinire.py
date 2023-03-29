class sensori:
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.lA = 0
        self.lD = 1
        self.lS = 2
        
        self.laserNum = 3
         
        self.laser = [sensore() for i in range(self.laserNum)] #[sensore()]*self.laserNum
        self.laser[self.lA].definisci(numero = self.lA, nome = "lA", pin = 21, indirizzo = 0x20)
        self.laser[self.lD].definisci(numero = self.lD, nome = "lD", pin = 20, indirizzo = 0x22)
        self.laser[self.lS].definisci(numero = self.lS, nome = "lS", pin = 16, indirizzo = 0x24)
        
        def Init(self)
            for index in range(self.laserNum): #inizializzazione GPIO laser
                GPIO.setup(self.laser[index].pin,GPIO.OUT)
                GPIO.output(self.laser[index].pin,GPIO.LOW)
            
            i2c = busio.I2C(board.SCL, board.SDA)
            
            for index in range(self.laserNum):
                GPIO.output(self.laser[index].pin,GPIO.HIGH) #attivo singolo laser
                print("start sensor", self.laser[index].nome)
            try:
                sensor = adafruit_vl6180x.VL6180X(i2c)
                sensor._write_8(0x212, self.laser[index].indirizzo) #cambio indirizzo singolo laser
                
            try:
                self.laser[index].misura = adafruit_vl6180x.VL6180X(i2c, self.laser[index].indirizzo) #inizializzo singolo laser e lo aggiungo alla lista
            except:
                pass
        
        def read(self,index)
        
        