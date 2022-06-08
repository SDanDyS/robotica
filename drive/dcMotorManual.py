import RPi.GPIO as GPIO          
from time import sleep
import threading
"""
manual controls to handle the robot only used for test purposes

"""
# Define pins
in1 = 6
in2 = 5
in3 = 13
in4 = 26
ena = 25
enb = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.setup(enb,GPIO.OUT)
p=GPIO.PWM(ena,1000)
p.start(25)
pb=GPIO.PWM(enb,1000)
pb.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("Use WASD to control, X to stop")
# print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    
temp1=1
"""
when the program is running different keystrokes start different actions to handle the robot
"""

while(1):
    """
        :param x : string 
            reads the keystroke input
        
    """

    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='x':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        x='z'

    elif x=='w':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(100)
        pb.ChangeDutyCycle(100)

        temp1=1
        x='z'

    elif x=='s':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        p.ChangeDutyCycle(100)
        pb.ChangeDutyCycle(100)

        temp1=0
        x='z'
    
    elif x=='a':
        print("left")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)   
        pb.ChangeDutyCycle(100)
        p.ChangeDutyCycle(100)
    
    elif x=='d':
        print("right")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)   
        pb.ChangeDutyCycle(100)
        p.ChangeDutyCycle(85)

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(65)
        pb.ChangeDutyCycle(65)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(100)
        pb.ChangeDutyCycle(100)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")