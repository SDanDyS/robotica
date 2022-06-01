import argparse
from vision.robotVision import *
from dashboard.dashboardServer import *
#from bt.jsonBt import *
from drive.dcMotorIndu import *
from threading import *
from weight.scale import *
import logging
import RPi.GPIO as GPIO
import time

# weight = Weight()
# weight.start()

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

# Start camera
if args["camera"] is not None:
    vision = RobotVision()
    vision.camSelector = args["camera"]
    vision.FLAG = 1
    vision.start()

# Start dashboard webserver
# dashboard = dashboardServer()
# dashboard.start()