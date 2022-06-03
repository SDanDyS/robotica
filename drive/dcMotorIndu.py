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
# pa=GPIO.PWM(ena,1000)
# pb=GPIO.PWM(enb,1000)
class dcMotorIndu(threading.Thread):
    selectedMotor = 0

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
        self.selectedMotor = motorId
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        # if left motor
        if motorId == 0:
            print("Init left motor")
            print(self.selectedMotor)
            
            GPIO.setup(in1,GPIO.OUT)
            GPIO.setup(in2,GPIO.OUT)
            GPIO.setup(ena,GPIO.OUT)
            self.pwm=GPIO.PWM(ena,1000)
        # right motor
        elif motorId == 1:
            print("Init right motor")
            print(self.selectedMotor)

            GPIO.setup(in3,GPIO.OUT)
            GPIO.setup(in4,GPIO.OUT)
            GPIO.setup(enb,GPIO.OUT)
            self.pwm=GPIO.PWM(enb,1000)

    def forward(self, speed):
        if self.selectedMotor == 0:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        elif self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        
        self.pwm.start(speed)         
            
    def backwards(self):
         if self.selectedMotor == 0:  
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
            self.pwm.start(100)
            self.pwm.start(100)
         if self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
            self.pwm.start(100)
            self.pwm.start(100)
        
    def right(self):
        
         if self.selectedMotor == 0:  
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
         if self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
            self.pwm.ChangeDutyCycle(25)
            self.pwm.ChangeDutyCycle(25)
        
    def left(self):
        if self.selectedMotor == 0:  
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        if self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)   
            self.pwm.ChangeDutyCycle(25)
            self.pwm.ChangeDutyCycle(25)
        
    def turbo(self):
        if self.selectedMotor == 0:
             GPIO.output(self.in1,GPIO.HIGH)
             GPIO.output(self.in2,GPIO.LOW)
        if self.selectedMotor == 1:
             GPIO.output(self.in3,GPIO.HIGH)
             GPIO.output(self.in4,GPIO.LOW)
        
             self.pwm.ChangeDutyCycle(100)
             self.pwm.ChangeDutyCycle(100)
        
    def rightmotor(self):
        
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        self.pwm.start(100)
        
    
    def leftmotor(self):
       
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwm.start(100)
    
    def achter1(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.start(100)
    
    def achter2(self):
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        self.pwm.start(100)
    
    
    def stop(self):
        if self.selectedMotor == 0:
             GPIO.output(self.in1,GPIO.LOW)
             GPIO.output(self.in2,GPIO.LOW)
        if self.selectedMotor == 1:
             GPIO.output(self.in3,GPIO.LOW)
             GPIO.output(self.in4,GPIO.LOW)
        
        
        
