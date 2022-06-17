import argparse
from vision.robotVision import *
from dashboard.dashboardServer import *
from bt.jsonBt import *
from drive.dcMotorIndu import *
from threading import *
#from weight.scale import *
import logging
import RPi.GPIO as GPIO
import time
# from weight.scale import *
from bt.i2c import *

import asyncio

class Robot():
    """
    Main function of the project
    """

    def __init__(self):
        """
        Initializes the program with the set arguments to run the program
        different arguments call different ways to handle the robot

        """
        # Set logging level (debug, info, warning, error, critical)
        logging.basicConfig(level=logging.DEBUG)

        # Grab arguments from Python command
        ap = argparse.ArgumentParser()
        # Select camera module; 'pi' grabs PiCamera, 0-9 grabs regular webcam camera. Defaults to 'pi'.
        ap.add_argument("-cam", "--camera", type=str, nargs='?', const ='pi', help='Enter \'pi\' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi')
        ap.add_argument("-flag", "--flag", type=str, const='1', nargs='?', help='flags for vision or dance')
        # Add -bt to set to True
        ap.add_argument("-bt", "--bluetooth", action="store_true", help='Enable the bluetooth receiver/sender')
        # Add -drive to enable manual motors
        ap.add_argument("-drive", "--enabledrive", action="store_true", help='Enable the manual drive mode')

        args = vars(ap.parse_args())

        self.bus = i2c()
        self.bus.start()

        # Start camera
        if  (args["camera"] and (args["flag"] == '1' or args["flag"] == '2' or args["flag"] == '3')):
            vision = RobotVision()
            vision.camSelector = args["camera"]
            vision.FLAG = int(args["flag"])
            vision.start()
        elif (args["flag"] == "3" or args["flag"] == "4"):
            print("Requesting something else")

        # Start bluetooth connection
        if args["bluetooth"] == True:
            self.motor_left = dcMotorIndu(0)
            self.motor_right = dcMotorIndu(1)

            bluetooth = btServer(self)

            bluetooth.start()
        
        # Start dashboard webserver
        dashboard = dashboardServer()
        dashboard.start()

        # Write sensor data to file for Dashboard
        async def write_data():
            while True:
                await asyncio.sleep(1)

                # Write Bluetooth
                if args["bluetooth"] == True:
                    btFile = open("btData", "w")
                    btFile.write(str(bluetooth.json))
                    btFile.close()

                # Write weight sensor data
                weightFile = open("weightData", "w")
                weightFile.write(str(self.bus.getWeight()))
                weightFile.close()

                # Write voltage data
                voltageFile = open("voltageData", "w")
                voltageFile.write(str(self.bus.getVoltage()))
                voltageFile.close()


        loop = asyncio.get_event_loop()
        cors = asyncio.wait([write_data()])
        loop.run_until_complete(cors)

if __name__ == "__main__":
    Robot()
