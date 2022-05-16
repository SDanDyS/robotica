import argparse
from vision.robotVision import *
from dashboard.dashboardServer import *
from bt.btConnection import *
from threading import *
import logging

logging.basicConfig(level=logging.DEBUG)

# Grab arguments from Python command
ap = argparse.ArgumentParser()
# Select camera module; 'pi' grabs PiCamera, 0-9 grabs regular webcam camera. Defaults to 'pi'.
ap.add_argument("-cam", "--camera", type=str, required=True, nargs='?', const='pi', help='Enter \'pi\' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi')
# Add -bt to set to True
ap.add_argument("-bt", "--bluetooth", action="store_true", help='Enable the bluetooth receiver/sender')
args = vars(ap.parse_args())

vision = robotVision()

# INVOKE THE THREAD. UPON PRESSING Q THE THREAD WILL TERMINATE.
# CREATE SOME SORT OF HANDLER IN CASE THE THREAD SHOULD START AGAIN
vision.camSelector = args["camera"]
vision.FLAG = 2
vision.start()
# robot.getFocalLength(248, 11, 24)
# robot.getFocalLength()
# print("Distance: " + str(robot.getDistance(800)))

# Start bluetooth connection
if args["bluetooth"] == True:
    bluetooth = btServer()
    bluetooth.start()

# Start dashboard webserver
dashboard = dashboardServer()
dashboard.start()

