import argparse
from vision.robotVision import *
from dashboard.dashboardServer import *
from bt.jsonBt import *
from drive.dcMotorIndu import *
from threading import *
import logging
import RPi.GPIO as GPIO
import time

class Robot():
    def __init__(self):
        # Set logging level (debug, info, warning, error, critical)
        logging.basicConfig(level=logging.DEBUG)

        # Grab arguments from Python command
        ap = argparse.ArgumentParser()
        # Select camera module; 'pi' grabs PiCamera, 0-9 grabs regular webcam camera. Defaults to 'pi'.
        ap.add_argument("-cam", "--camera", type=str, nargs='?', const='pi', help='Enter \'pi\' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi')
        # Add -bt to set to True
        ap.add_argument("-bt", "--bluetooth", action="store_true", help='Enable the bluetooth receiver/sender')
        # Add -drive to enable manual motors
        ap.add_argument("-drive", "--enabledrive", action="store_true", help='Enable the manual drive mode')

        args = vars(ap.parse_args())

        # Robot vars
        self.ly = 0
        self.lx = 0
        self.ly = 0
        self.rx = 0

        # Start camera
        if args["camera"] == True:
            vision = robotVision()
            vision.camSelector = args["camera"]
            vision.FLAG = 2
            vision.start()
            
        # dcMotorIndu.forward(1)
        # 
        # # Start bluetooth connection
        if args["bluetooth"] == True:
            self.motor_left = dcMotorIndu(0)
            self.motor_right = dcMotorIndu(1)

            self.bluetooth = btServer(self)

            # bluetooth = btServer(motor_left, motor_right)
            self.bluetooth.run()
        #     bluetooth.forward(25)


        # Start motor drive
        # if args["enabledrive"] == True:

        # Start dashboard webserver
        dashboard = dashboardServer()
        dashboard.start()

if __name__ == "__main__":
    Robot()