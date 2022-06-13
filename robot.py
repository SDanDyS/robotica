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

import asyncio

class Robot():
    """
    main function of the project

    """
    ly = 0

    def __init__(self):
        """
        initializes the program with the set arguments to run the program
        different arguments call different ways to handle the robot

        """
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
        if args["camera"] == 'pi':
            print(args["camera"])
            vision = RobotVision()
            vision.camSelector = args["camera"]
            vision.FLAG = 2
            vision.start()
            # time.sleep(10)
            # vision.releaseRobot()
            
        # Start bluetooth connection
        if args["bluetooth"] == True:
            self.motor_left = dcMotorIndu(0)
            self.motor_right = dcMotorIndu(1)

            bluetooth = btServer(self)

            # bluetooth = btServer(motor_left, motor_right)
            bluetooth.start()

            #temp test
            async def read_val():
                while True:
                    await asyncio.sleep(1)
                    print("-=-=-=-=-=-=-=-=-=-=-=-")
                    print("[robot.py] Bluetooth values:")
                    print(bluetooth.ly)
                    print(bluetooth.lx)
                    print(bluetooth.ry)
                    print(bluetooth.rx)
                    print("Connected:")
                    print(bluetooth.connected)
                    print(("-=-=-=-=-=-=-=-=-=-=-=-"))
                    # self.ly = bluetooth.ly
                    # my_list.append(random.random())
                    # notify()

            loop = asyncio.get_event_loop()
            cors = asyncio.wait([read_val()])
            loop.run_until_complete(cors)

        # Start dashboard webserver
        dashboard = dashboardServer()
        dashboard.start()

if __name__ == "__main__":
    Robot()
