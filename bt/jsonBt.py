from bluetooth import *
from multiprocessing import Process
import time
import re
import RPi.GPIO as GPIO
from time import sleep
import json
import logging
import threading
import bt.i2c as bus
# from bt import i2c as bus
from bt.i2c import *
#from vision.robotVision import *
from drive.dance import *


sock = BluetoothSocket(RFCOMM)


class btServer(threading.Thread):
    def __init__(self, shared):
        '''
        Constructs the btServer class.

                Parameters:
                        shared (object): Shared objects from robot.py, containing left and right DC motors.
        '''
        super(btServer, self).__init__()

        self.motor_left = shared.motor_left
        self.motor_right = shared.motor_right

        self.bus = shared.bus

    def sender(self, input):
        '''
        Sends data (input) to the Bluetooth controller.

                Parameters:
                        input (string): String to be sent to controller
        '''

        while True:
            #data = input()
            # if len(data) == 0: break
            data = 1
            # time.sleep(4)
            sock.send(i2c.getWeight())
            print(i2c.getWeight())
            sock.send("\n")
            sock.send(i2c.getVoltage())
            sock.send("\n")

    ly = 0
    lx = 0
    ry = 0
    rx = 0
    connected = False
    json = {}

    # Default controller values; 4095 - 0
    HIGH_VALUE = 4000
    LOW_VALUE = 100

    def receiver(self):
        '''
        Processes the data received by the Bluetooth controller and controls DC motors.
        '''
        flag = 0
        driveorGrip = 0

        stop_vision_thread = False
        stop_dance_thread = False
#         r = RobotVision()
#         r.start()
        d = dance(self.motor_left, self.motor_right)
        start_vision = False

        while True:
            try:
                data = sock.recv(self.buf_size)
            except:
                print("exception reached")
                self.run()
                break

            # Check whether data was received
            if not data:
                logging.error("Didn't receive data, check connection")
                break

            # Check whether received data is valid JSON, skip if invalid
            utfData = data.decode("utf-8")
            try:
                if not utfData:
                    break
                parsedData = json.loads(utfData)
                logging.info(parsedData)
            except ValueError:
                logging.error("Received invalid JSON, skipping...")
                continue

            # Parse and store joystick coordinates
            ly = int(parsedData["LY"])
            lx = int(parsedData["LX"])
            ry = int(parsedData["RY"])
            rx = int(parsedData["RX"])
            flag = int(parsedData["flag"])
            driveorGrip = int(parsedData["driveOrGrip"])

            # Expose to robot.py
            self.ly = ly
            self.lx = lx
            self.ry = ry
            self.rx = rx
            self.json = parsedData

            if (flag == 0):
                stop_vision_thread = True
                stop_dance_thread = True

                try:
                    r.join()
                except:
                    pass
            elif (flag == 1):
                stop_dance_thread = True
                stop_vision_thread = False

                try:
                    r.FLAG = flag##SET FLAGS OUTSIDE OF TRY CATCH
                    r.start()
                except:
                    pass

            elif (flag == 2):
                stop_dance_thread = True
                stop_vision_thread = False

                try:
                    r.FLAG = flag
                    r.start()
                except:
                    pass
            elif (flag == 3):
                stop_dance_thread = False
                stop_vision_thread = True
                try:
                    d.spin(self.motor_left,self.motor_right)
                    time.sleep(2)
                    d.forward(self.motor_left,self.motor_right)
                    time.sleep(2)
                    self.bus.lowerHeight()
                    time.sleep(3)
                    self.bus.closeGrabber()
                    time.sleep(0.5)
                    self.bus.openGrabber()
                    time.sleep(0.5)
                    self.bus.raiseHeight()
                    time.sleep(2)
                    d.switch(self.motor_left,self.motor_right)
                    d.sidetoside(self.motor_left,self.motor_right)
                    d.forward_backwards(self.motor_left,self.motor_right)
                    self.motor_left.forward(20)
                    time.sleep(1.5)
                    self.motor_right.forward(20)
                    time.sleep(3)
                    self.motor_left.forward(20)
                    time.sleep(1.5)
                    
                    
                    
                except:
                     pass
            elif (flag == 4):
                try:
                    d.linedance(self.bus.beat)
                    self.bus.beat = False
                except:
                    pass
                # TODO create an object which would
                # listen to music and dance on it
            if(driveorGrip == 1 or driveorGrip == 2):
                # stop_vision_thread = True
                # stop_dance_thread = True
                # Driver mode
                if (driveorGrip == 1):
                    # Stop right motor
                    if ry > 1920 and ry < 2150:
                        self.motor_right.stop()
                    # Stop left motor
                    if ly > 1900 and ly < 2150:
                        self.motor_left.stop()

                    # Motors both backwards
                    if (ly < 1 and ry < 1):
                        self.motor_left.backwards(100)
                        self.motor_right.backwards(100)

                    # Forward
                    if ry == 4095 and ly == 4095:
                        self.motor_left.forward(100)
                        self.motor_right.forward(100)

                    # Left motor backwards
                    if ly < 1:
                        self.motor_left.backwards(100)
                    # Right motor backwards
                    if ry < 1:
                        self.motor_right.backwards(100)
                    # Right
                    if ly == 4095 and ry == 0:
                        self.motor_left.forward(100)
                        self.motor_right.backwards(100)
                    # Left
                    if ly < 1 and ry > 4000:
                        self.motor_left.backwards(100)
                        self.motor_right.forward(100)

                    # Left motor forward
                    if ly == 4095 and 1900 < ry < 2150:
                        self.motor_left.forward(100)

                    # Right motor forward
                    if ry == 4095 and 1900 < ly < 2150:
                        self.motor_right.forward(100)

                    if 2151 < ry < 4095:
                        self.motor_right.forward(25)
                    if 2151 < ly < 4095:
                        self.motor_left.forward(25)
                    if 1 < ry < 1850:
                        self.motor_right.backwards(25)
                    if 1 < ly < 1850:
                        self.motor_left.backwards(25)

                # Grabber Mode
                elif (driveorGrip == 2):
                    # r.join()
                    self.heightArm(ly)
                    self.grabber(rx)

    # Raise, lower and stop the height of the arm
    def heightArm(self, ly):
        if ly > self.HIGH_VALUE:
            self.bus.raiseHeight()
        elif ly <= self.HIGH_VALUE and ly >= self.LOW_VALUE:
            self.bus.stopHeight()
        elif ly < self.LOW_VALUE:
            self.bus.lowerHeight()

    # Open, close and stop the grabber
    def grabber(self, rx):
        if rx > self.HIGH_VALUE:
            self.bus.openGrabber()
        elif rx <= self.HIGH_VALUE and rx >= self.LOW_VALUE:
            self.bus.stopGrabber()
        elif rx < self.LOW_VALUE:
            self.bus.closeGrabber()

    def receiveData():
        bus.receiveData()

    def run(self):
        '''
        Sets up the Bluetooth connection & execute new thread to process incoming data.
        '''

        # MAC address of ESP32
        addr = "C8:C9:A3:C5:7A:E2"

        # Find controller
        # def connect_bt()
        service_matches = find_service(address=addr)

        self.buf_size = 256

        if len(service_matches) == 0:
            logging.error("Something went wrong with the bluetooth connection")
            self.connected = False
            while True:
                try:
                    self.run()
                except:
                    break

            # sys.exit(0)

        for s in range(len(service_matches)):
            logging.debug("\nservice_matches: [" + str(s) + "]:")
            logging.debug(service_matches[s])

        # while len(service_matches) == 1:
            # print("while == 1 true")
        try:
            print("try first_match")
            first_match = service_matches[0]
        except:
            print("except reached service_matches[0]")
            self.run()
            # break
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port = 1

        # Create the client socket
        sock.connect((host, port))
        self.connected = True

        # sender = Process(target=self.sender)
        # sender.start()

        # receiver = Process(target=self.receiver)
        # receiver.start()

        self.receiver()

    def active(self):
        '''
        Returns state of Bluetooth connection.

                Returns:
                        boolean: Connected True/False
        '''
        if sock.connect((host, port)) == True:
            return True
        else:
            return False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted, shutting down program")
        pa.stop()
        sock.close()
        sys.exit(0)
        pass
