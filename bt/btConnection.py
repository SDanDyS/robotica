from bluetooth import *
import threading
import time
import logging
import re

class btServer(threading.Thread):
    def run(self):
        # Send data to remote control
        def send():
            while True:
                #data = input()
                #if len(data) == 0: break
                data = 1
                        
                #sock.send(str(data))
                sock.send("ahoi")
                sock.send("\n")
        
        # Receive data from remote control        
        def receive():
            while True:
                data = sock.recv(buf_size)
                #if data:
                #time.sleep(0.1)
                numeric_string = re.sub("[^0-9]","",data.decode("utf-8"))

                logging.debug(numeric_string)
                
                if not data: break
                #logging.debug(data)

        #MAC address of ESP32
        addr = "84:CC:A8:69:97:D2"
        #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        #service_matches = find_service( uuid = uuid, address = addr )
        service_matches = find_service( address = addr )

        buf_size = 32;

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
        logging.info("connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
        sock=BluetoothSocket(RFCOMM)
        sock.connect((host, port))

        logging.info("Bluetooth connected!")
    
        send_thread = threading.Thread(target=send)
        receive_thread = threading.Thread(target=receive)
        
        send_thread.start()
        receive_thread.start()