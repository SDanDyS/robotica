from dcMotorIndu import *
import time

class dance():
    motor_left = dcMotorIndu(0)
    motor_right = dcMotorIndu(1)
    
    def spin():       
        motor_left.forward()
        motor_right.backwards()
        
    def forward_backwards():
        motor_left.forward()
        motor_right.forward()
        time.sleep(2)
        motor_left.backwards()
        motor_right.backwards()
        time.sleep(2)
        
    def sidetoside():
        motor_left.forward()
        motor_right.backwards()
        time.sleep(1)
        motor_right.forward()
        motor_left.backwards()
        time.sleep(1)
        
    def switch():
        motor_left.forward()
        motor_right.backwards()
        time.sleep(2)
        motor_left.forward()
        motor_right.forward()
        time.sleep(2)
        motor_left.backwards()
        motor_right.backwards()
        time.sleep(2)
        motor_right.forward()
        motor_left.backwards()
        time.sleep(2)
        
    
    def linedance():
        #autonome dans
        #deze dans moet binnen 3 gebieden uitgevoerd worden en op de maat
        area = 0
        if 0 < area < 200:
            #move 1
            return 0
        if 200 < area 400:
            #move2
            return 1
        if 400 < area 600:
            #move3
            return 2
    def performing():
        