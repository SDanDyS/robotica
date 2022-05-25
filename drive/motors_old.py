import RPi.GPIO as GPIO          
from time import sleep
import threading

class motors(threading.Thread):
    def __init__(self,pin1,pin2,pin3,pin4,pin5,pin6):
        super().__init__()
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.pin5 = pin5
        self.pin6 = pin6

    def run(self):
        temp1=1

        GPIO.output(self.pin1,GPIO.LOW)
        GPIO.output(self.pin2,GPIO.LOW)
        GPIO.output(self.pin3,GPIO.LOW)
        GPIO.output(self.pin4,GPIO.LOW)
        pa=GPIO.PWM(self.pin5,1000)
        pb=GPIO.PWM(self.pin6,1000)
        pa.start(25)
        pb.start(25)
        print("\n")
        print("The default speed & direction of motor is LOW & Forward.....")
        print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
        print("\n")    

        while(1):

            x=input()
            
            if x=='r':
                print("run")
                if(temp1==1):
                 GPIO.output(self.pin1,GPIO.HIGH)
                 GPIO.output(self.pin2,GPIO.LOW)
                 print("forward")
                 x='z'
                else:
                 GPIO.output(self.pin1,GPIO.LOW)
                 GPIO.output(self.pin2,GPIO.LOW)
                 print("backward")
                 x='z'


            elif x=='s':
                print("stop")
                GPIO.output(self.pin1,GPIO.LOW)
                GPIO.output(self.pin2,GPIO.LOW)
                x='z'

            elif x=='f':
                print("forward")
                GPIO.output(self.pin1,GPIO.HIGH)
                GPIO.output(self.pin2,GPIO.LOW)
                temp1=1
                x='z'

            elif x=='b':
                print("backward")
                GPIO.output(self.pin1,GPIO.LOW)
                GPIO.output(self.pin2,GPIO.HIGH)
                temp1=0
                x='z'

            elif x=='l':
                print("low")
                pa.ChangeDutyCycle(25)
                x='z'

            elif x=='m':
                print("medium")
                pa.ChangeDutyCycle(50)
                x='z'

            elif x=='h':
                print("high")
                pa.ChangeDutyCycle(100)
                x='z'
                
            elif x=='t':
                if(temp1==1):
                     GPIO.output(self.pin3,GPIO.HIGH)
                     GPIO.output(self.pin4,GPIO.LOW)
                     print("forward")
                     x='z'
                else:
                     GPIO.output(self.pin3,GPIO.LOW)
                     GPIO.output(self.pin4,GPIO.HIGH)
                     print("backward")
                     x='z' 
            elif x=='n':
                print("forward")
                GPIO.output(self.pin3,GPIO.HIGH)
                GPIO.output(self.pin4,GPIO.LOW)
                temp1=1
                x='z'
            elif x=='z':
                print("low")
                pb.ChangeDutyCycle(25)
                x='z'    
            elif x=='k':
                print("high")
                pb.ChangeDutyCycle(100)
                x='z'
            elif x=='a':
                print("stop")
                GPIO.output(self.pin3,GPIO.LOW)
                GPIO.output(self.pin4,GPIO.LOW)
                x='z'
            elif x=='e':
                GPIO.cleanup()
                break
            
            
            else:
                print("<<<  wrong data  >>>")
                print("please enter the defined data to continue.....")