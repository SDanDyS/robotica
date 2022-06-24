import RPi.GPIO as GPIO          
from time import sleep
import threading
import re

in1 = 5
in2 = 6
in3 = 13
in4 = 26
ena = 25
enb = 12
# pa=GPIO.PWM(ena,1000)
# pb=GPIO.PWM(enb,1000)
class dcMotorIndu(threading.Thread):
    """
     this class represents the individual dcmotors

     selectedMotor : int
        gives an integer to the specific dcmotors which are 0 or 1
        in1-4 : int
            the selected pins used to use the dc motor
        ena/enb : int
            pint for the remote controller
    """
    in1 = 5
    in2 = 6
    in3 = 13
    in4 = 26
    ena = 25
    enb = 12
    selectedMotor = 0
    
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
        
    def __init__(self, motorId):
        """

        :param motorId: int
            gives an integer to the specific dcmotors which are 0 or 1
        :param selectedMotor: int
            gives an integer to the specific dcmotors which are 0 or 1
        """
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
            self.pwm=GPIO.PWM(ena,100)
        # right motor
        elif motorId == 1:
            print("Init right motor")
            print(self.selectedMotor)

            GPIO.setup(in3,GPIO.OUT)
            GPIO.setup(in4,GPIO.OUT)
            GPIO.setup(enb,GPIO.OUT)
            self.pwm=GPIO.PWM(enb,100)

    def forward(self, speed = 100):
        """
        :param speed:int
            integer to set the speed when calling the function
        :return:
        """
        if self.selectedMotor == 0:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        elif self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)

        self.pwm.start(speed)         
            
    def backwards(self, speed = 100):
        """
        function called when the joysticks go backwards
        :return:
        none
        """
        if self.selectedMotor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
            self.pwm.start(speed)
        elif self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
            self.pwm.start(speed)

    def stop(self):
        """
        gets called when the robots needs to stop
        :param self:
        :return:
        none
        """
        if self.selectedMotor == 0:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
        if self.selectedMotor == 1:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)



