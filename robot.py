import argparse
from vision.robotVision import *
from dashboard.dashboardServer import *
from bt.jsonBt import *
from drive.dcMotorIndu import *
from threading import *
from weight.scale import *
import logging
import RPi.GPIO as GPIO
import time


# Grab arguments from Python command
# 'pi' grabs PiCamera, 0-9 grabs regular webcam camera. Defaults to 'pi'.
# ap = argparse.ArgumentParser()
# ap.add_argument("-cam", "--camera", type=str, required=True,
#                 help='Enter \'pi\' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi.')
# args = vars(ap.parse_args())

# vision = robotVision()
# 
# # INVOKE THE THREAD. UPON PRESSING Q THE THREAD WILL TERMINATE.
# # CREATE SOME SORT OF HANDLER IN CASE THE THREAD SHOULD START AGAIN
# vision.camSelector = args["camera"]
# vision.FLAG = 1
# vision.start()
weight = Weight()
weight.start()

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
if args["camera"] == True:
    vision = robotVision()
    vision.camSelector = args["camera"]
    vision.FLAG = 2
    vision.start()

# motor_left = dcMotorIndu(0)
# motor_right = dcMotorIndu(1)
# dcMotorIndu.run(1)
# 
# # Start bluetooth connection
if args["bluetooth"] == True:
    bluetooth = btServer(motor_left, motor_right)
    bluetooth.forward(25)

# if vision ziet == true
# motor1.forward

# if distance == 2
# motor1.stop
# Start motor drive
# if args["enabledrive"] == True:
#     drive = motors(in1,in2,in3,in4,ena,enb)
#     drive.start()
# motor1 = dcMotor(0)
# motor1.right()
# time.sleep(2)
# motor1.stop()
# time.sleep(10)
# motor1.turbo()
# time.sleep(4)
# motor1.stop()

# Start dashboard webserver
dashboard = dashboardServer()
dashboard.start()