import RPi.GPIO as GPIO          
from time import sleep
import threading
import re

in1 = 6
in2 = 5
in3 = 13
in4 = 26
ena = 25
enb = 12


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

pa=GPIO.PWM(ena,1000)
pb=GPIO.PWM(enb,1000)
class dcMotor(threading.Thread):
    in1 = 6
    in2 = 5
    in3 = 13
    in4 = 26
    ena = 25
    enb = 12
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
        
    def __init__(self, motorId):
        super().__init__()
        self.motorId = motorId
        
        # if left motor
        if motorId == 0:
            print("Init left motor")
            
            #GPIO.setup(self.in2,GPIO.OUT)
            #GPIO.setup(self.en1,GPIO.OUT)
            #GPIO.output(self.in1,GPIO.HIGH)
            #GPIO.output(self.in2,GPIO.LOW)
            #GPIO.setup(self.in3,GPIO.OUT)
            #GPIO.setup(self.in4,GPIO.OUT)
#             GPIO.setup(self.enb,GPIO.OUT)
            #GPIO.output(self.in3,GPIO.HIGH)
            #GPIO.output(self.in4,GPIO.LOW)
            #pa.start(100)
            #pb.start(100)
            
            
        # right motor
        elif motorId == 1:
            print("Init right motor")
#             GPIO.setup(self.in3,GPIO.OUT)
#             GPIO.setup(self.in4,GPIO.OUT)
#             GPIO.setup(self.enb,GPIO.OUT)
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)
            #pb=GPIO.PWM(self.enb,1000)
            pb.start(25)

            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)

    def forward(self, speed):
        
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        #pa=GPIO.PWM(self.ena,1000)
        #pb=GPIO.PWM(self.enb,1000)
        pa.start(speed)
        pb.start(speed)
            
    def backwards(self):
             
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        pa.start(25)
        pb.start(25)
        
    def right(self):
        
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
            
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        pa.ChangeDutyCycle(25)
        pb.ChangeDutyCycle(25)
        
    def left(self):
             
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
            
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        pa.ChangeDutyCycle(25)
        pb.ChangeDutyCycle(25)
        
    def turbo(self):
        
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        #pa=GPIO.PWM(self.ena,1000)
        #pb=GPIO.PWM(self.enb,1000)
        pa.ChangeDutyCycle(100)
        pb.ChangeDutyCycle(100)
        
    def rightmotor(self):
        
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        pb.start(100)
        
    
    def leftmotor(self):
        
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        pa.start(100)
    
    
    def stop(self):
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
            
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        pa.ChangeDutyCycle(0)
        pb.ChangeDutyCycle(0)
        
        
        
