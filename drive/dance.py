# from dcMotorIndu import *
import time

class dance():
    danceCount = 0

    def __init__(self, motor1,motor2):
        self.motor1 = motor1
        self.motor2 = motor2
    
    
    
    def spin(self,motor1,motor2):       
        self.motor1.forward()
        self.motor2.backwards()
        time.sleep(2)
        self.motor1.stop()
        self.motor2.stop()
        
    def forward_backwards(self, motor1,motor2):
        self.motor2.forward()
        self.motor2.forward()
        time.sleep(2)
        self.motor1.backwards()
        self.motor2.backwards()
        time.sleep(2)
        self.motor1.stop()
        self.motor2.stop()
        
    def forward(self, motor1,motor2):
        self.motor1.forward()
        self.motor2.forward()
        time.sleep(0.2)
        self.motor1.forward()
        self.motor2.forward()
        time.sleep(0.2)
        self.motor1.stop()
        self.motor2.stop()
        
    def sidetoside(self, motor1,motor2):
        self.motor1.forward()
        self.motor2.backwards()
        time.sleep(1)
        self.motor2.forward()
        self.motor1.backwards()
        time.sleep(1)
        self.motor1.stop()
        self.motor2.stop()
        
    def switch(self, motor1,motor2):
        self.motor1.forward()
        self.motor2.backwards()
        time.sleep(2)
        self.motor1.forward()
        self.motor2.forward()
        time.sleep(2)
        self.motor1.backwards()
        self.motor2.backwards()
        time.sleep(2)
        self.motor2.forward()
        self.motor1.backwards()
        time.sleep(2)
        self.motor1.stop()
        self.motor2.stop()
        
    
    def linedance(self, beat):
        #autonome dans
        #deze dans moet binnen 3 gebieden uitgevoerd worden en op de maat
        if not beat:
            return

        if self.danceCount == 0:
            self.spin()
        elif self.danceCount == 1:
            self.forward_backwards()
        elif self.danceCount == 2:
            self.forward()
        elif self.danceCount == 3:
            self.sidetoside()
        elif slef.danceCount == 4:
            self.switch()

        self.danceCount += 1

        if danceCount >= 6:
            self.danceCount = 0

        
#     def performing():
        