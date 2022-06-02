from bluetooth import *
from multiprocessing import Process
import time
import re
import RPi.GPIO as GPIO          
from time import sleep
import json
import logging

sock=BluetoothSocket(RFCOMM)

class btServer():
    def __init__(self, motor_left, motor_right):
        # self.shared = sharedRobot
        # print(sharedRobot.motor_left)
        self.motor_left = motor_left
        print(self.motor_left)
        # print(self.motor_left)
        self.motor_right = motor_right
        print(self.motor_right)

    #versturen
    def input_and_send(self):

        #print("\nType something\n")
        while True:
            #data = input()
            #if len(data) == 0: break
            data = 1
            # time.sleep(40)
            sock.send("ahoi")
            sock.send("\n")
    #ontvangen        
    def rx_and_echo(self):
        ly = 0
        lx = 0
        ry = 0
        rx = 0
    
        while True:
            data = sock.recv(self.buf_size)

            if not data: break
            
            utfData = data.decode("utf-8")

            try:
                if not utfData: break
                parsedData = json.loads(utfData)
                #print("parsedData:")
                print(parsedData)
            except ValueError:
                print("Received invalid JSON, skipping...")
                continue
            
            ly = int(parsedData["LY"])
            lx = int(parsedData["LX"])
            ry = int(parsedData["RY"])
            rx = int(parsedData["RX"])

#             # self.shared.ly = ly
#             # self.shared.lx = lx
#             # self.shared.ry = ry
#             # self.shared.rx = rx

            # if ly > 4000:
            #     self.motor_left.forward(100)
            #     self.motor_right.forward(100)
            # else:
            #     self.motor_right.stop()
            #     self.motor_left.stop()

            
             #vooruit                   
#             if ry < 3000 and ry > 2500 and ly > 2500 and ly < 3000 :
#                 print("self.motor_left.forward(25)")
#                 #changeMotorSpeed(50)
#                 self.motor_left.forward(25)
                #achteruit
            if ry < 500 and ly < 500:
                print("self.motor_left.backwards()")
                self.motor_left.backwards()
                self.motor_right.backwards() 
                #stop
            if ry > 1920 and ry < 1990 and ly>1900 and ly < 1980:
                print("self.motor_left.stop()")
                self.motor_right.stop()
                self.motor_left.stop()
                print(self.motor_left)
                print(self.motor_right)


#                  Ssnel
            if ry>4000 and ly > 4000:
                print("beide motoren")
                self.motor_left.forward(100)
                self.motor_right.forward(100)
               #rechts
            if ry > 4000 and ly < 1:
                print("self.motor_left.right()")
                self.motor_left.achter1()
                self.motor_right.rightmotor() 
                 
                 #links
            if ry < 1 and ly > 4000:
                print("links")
                self.motor_left.leftmotor()
                self.motor_right.achter2()
            if ly==4095 and 1900 < ry <1990:
               
                print("linkermotor")
                self.motor_left.leftmotor()
#                 self.motor_left.stop()
            
            if ry==4095 and 1900 < ly <1990:
                print("rechtemotor")
                self.motor_right.rightmotor()
    
    def run(self):

        #MAC address of ESP32
        addr = "C8:C9:A3:C5:7A:E2"
        #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        #service_matches = find_service( uuid = uuid, address = addr )
        service_matches = find_service( address = addr )

        self.buf_size = 64;

        if len(service_matches) == 0:
            logging.error("Something went wrong with the bluetooth connection")
            sys.exit(0)

        for s in range(len(service_matches)):
            print("\nservice_matches: [" + str(s) + "]:")
            print(service_matches[s])
            
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port=1
        self.motor_left.forward(100)
        self.motor_right.forward(100)


        # Create the client socket
#         sock=BluetoothSocket(RFCOMM)
        sock.connect((host, port))

        # proc1 = Process(target=self.input_and_send)
        # proc1.start()

        # proc2 = Process(target=self.rx_and_echo)
        # proc2.start()
        self.rx_and_echo()

        print("connected")

    
    def changeMotorSpeed(speed):
        print("Set speed to %s", speed)
        pa.ChangeDutyCycle(speed)

    def active(self):
        if sock.connect((host, port)) == True:
            return "actief"
        else:
            return "non actief"
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted, shutting down program")
        pa.stop()
        sock.close()
        sys.exit(0)
        pass