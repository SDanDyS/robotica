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
#         GPIO.output(self.in1,GPIO.HIGH)
#         GPIO.output(self.in2,GPIO.LOW)
#         GPIO.output(self.in3,GPIO.HIGH)
#         GPIO.output(self.in4,GPIO.LOW)
        #pa=GPIO.PWM(self.ena,1000)
        #pb=GPIO.PWM(self.enb,1000)
#         pa.start(speed)
#         pb.start(speed)
            
    def backwards(self):
             
#         GPIO.output(self.in1,GPIO.LOW)
#         GPIO.output(self.in2,GPIO.HIGH)
#         GPIO.output(self.in3,GPIO.LOW)
#         GPIO.output(self.in4,GPIO.HIGH)
#         pa.start(25)
#         pb.start(25)
        
    def right(self):
        
#         GPIO.output(self.in1,GPIO.HIGH)
#         GPIO.output(self.in2,GPIO.LOW)
#             
#         GPIO.output(self.in3,GPIO.LOW)
#         GPIO.output(self.in4,GPIO.HIGH)
#         pa.ChangeDutyCycle(25)
#         pb.ChangeDutyCycle(25)
        
    def left(self):
             
#         GPIO.output(self.in1,GPIO.LOW)
#         GPIO.output(self.in2,GPIO.HIGH)
#             
#         GPIO.output(self.in3,GPIO.HIGH)
#         GPIO.output(self.in4,GPIO.LOW)
#         pa.ChangeDutyCycle(25)
#         pb.ChangeDutyCycle(25)
        
    def turbo(self):
        
#         GPIO.output(self.in1,GPIO.HIGH)
#         GPIO.output(self.in2,GPIO.LOW)
#         GPIO.output(self.in3,GPIO.HIGH)
#         GPIO.output(self.in4,GPIO.LOW)
        #pa=GPIO.PWM(self.ena,1000)
        #pb=GPIO.PWM(self.enb,1000)
#         pa.ChangeDutyCycle(100)
#         pb.ChangeDutyCycle(100)
        
    def rightmotor(self):
        
#         GPIO.output(self.in3,GPIO.HIGH)
#         GPIO.output(self.in4,GPIO.LOW)
#         pb.start(100)
        
    
    def leftmotor(self):
        
#         GPIO.output(self.in1,GPIO.HIGH)
#         GPIO.output(self.in2,GPIO.LOW)
#         pa.start(100)
    
    
    def stop(self):
        
#         GPIO.output(self.in1,GPIO.LOW)
#         GPIO.output(self.in2,GPIO.LOW)
#             
#         GPIO.output(self.in3,GPIO.LOW)
#         GPIO.output(self.in4,GPIO.LOW)
#         pa.ChangeDutyCycle(0)
#         pb.ChangeDutyCycle(0)
        
        
        
