from bluetooth import *
from multiprocessing import Process
import time
import re
import RPi.GPIO as GPIO          
from time import sleep
import json
import logging
import threading


sock=BluetoothSocket(RFCOMM)

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

    def sender(self, input):
        '''
        Sends data (input) to the Bluetooth controller.

                Parameters:
                        input (string): String to be sent to controller
        '''

        while True:
            #data = input()
            #if len(data) == 0: break
            data = 1
            # time.sleep(4)
            sock.send(input)
            sock.send("\n")

    ly = 0
    lx = 0
    ry = 0
    rx = 0
    connected = False

    def receiver(self):
        '''
        Processes the data received by the Bluetooth controller and controls DC motors.
        '''
        # ly = 0
        # lx = 0
        # ry = 0
        # rx = 0
        flag = 0
        driveorGrip = 0

        stop_vision_thread = False
        stop_dance_thread = False
        lock = False
        
        while True:
            data = sock.recv(self.buf_size)

            # Check whether data was received
            if not data:
                logging.error("Didn't receive data, check connection")
                break
            
            # Check whether received data is valid JSON, skip if invalid
            utfData = data.decode("utf-8")
            try:
                if not utfData: break
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

            # Set for robot.py
            self.ly = ly
            self.lx = lx
            self.ry = ry
            self.rx = rx
            
            if (flag == 1):
                 stop_dance_thread = True
                 stop_vision_thread = False
                 if (lock == False):
                    r = RobotVision()
                    r.FLAG = flag
                    r.start()
                    lock = True
            elif (flag == 2):
                r.FLAG = flag
            elif (flag == 3):
                stop_dance_thread = False
                stop_vision_thread = True
                ## TODO: create dance object
            elif (flag == 4):
                #TODO create an object which would
                # listen to music and dance on it 
            elif (driveorGrip == 1 or driveorGrip == 2):
                stop_vision_thread = False
                stop_dance_thread = False

                if (driveorGrip == 1):
                    # Stop right motor
                    if ry > 1920 and ry < 1990:
                        self.motor_right.stop()
                    # Stop left motor
                    if ly > 1900 and ly < 1980:
                        self.motor_left.stop()
                    # Forward
                    if ry > 4000 and ly > 4000:
                        self.motor_left.forward(100)
                        self.motor_right.forward(100)
                    # Motors both backwards
                    if (ly < 1 and ry < 1):
                        self.motor_left.backwards()
                        self.motor_right.backwards()
                    # Left motor backwards
                    if ly < 1:
                        self.motor_left.backwards()
                    # Right motor backwards
                    if ry < 1:
                        self.motor_right.backwards()
                    # Right
                    if ry == 4095 and ly == 0:
                        self.motor_left.right()
                        self.motor_right.right()  
                    #Left
                    if ry < 1 and ly > 4000:
                        self.motor_left.left()
                        self.motor_right.left()

                    # Left motor forward
                    if ly == 4095 and 1900 < ry < 1990:
                        self.motor_left.forward(100)

                    # Right motor forward
                    if ry == 4095 and 1900 < ly < 1990:
                        self.motor_right.forward(100)

                print(CatchMe)
            if driveorGrip == 2:
                print("armfunctie")
                

    def run(self):
        '''
        Sets up the Bluetooth connection & execute new thread to process incoming data.
        '''

        # MAC address of ESP32
        addr = "C8:C9:A3:C5:7A:E2"

        # Find controller
        service_matches = find_service( address = addr )

        self.buf_size = 256

        if len(service_matches) == 0:
            logging.error("Something went wrong with the bluetooth connection")
            self.connected = False
            sys.exit(0)

        for s in range(len(service_matches)):
            logging.debug("\nservice_matches: [" + str(s) + "]:")
            logging.debug(service_matches[s])
            
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port=1

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