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
    def __init__(self, motor):
        self.motor = motor

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
#        
#         sock.send("\nsend anything\n")
                
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
            
             #vooruit                   
#             if ry < 2500 and ry > 2000 and ly < 2500 and ly > 2000 :
#                  #print("rx < 1000")
#                  #changeMotorSpeed(50)
#                  self.motor.forward(25)
                #achteruit
            if ry < 500 and ly < 500:
                 self.motor.backwards()    
                 #stop
            elif ry <1880 and ry < 1950 and ry>1700 and ly > 1700:
                 self.motor.stop()
#                  Ssnel
            elif ry>4000 and ly > 4000:
                
                self.motor.forward(100)
                
               #rechts
            elif ry > 3000 and ly < 1000:
                 self.motor.right()
                 
                 #links
            elif ry < 1000 and ly > 3000:
                 self.motor.left()
            
            #elif ry > 3500:
                 #self.motor.rightmotor()
            
            #elif ly > 3500:
#                  self.motor.leftmotor()
    
#             elif rx >= 1000:
#                 #print("rx >= 1000")
#                 #changeMotorSpeed(25)
#                 pa.ChangeDutyCycle(0)
    
    def run(self):
        #MAC address of ESP32
        addr = "84:CC:A8:69:97:D2"
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
        print("connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
#         sock=BluetoothSocket(RFCOMM)
        sock.connect((host, port))
        
        proc1 = Process(target=self.input_and_send)
        proc1.start()

        proc2 = Process(target=self.rx_and_echo)
        proc2.start()

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