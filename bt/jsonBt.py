from bluetooth import *
from multiprocessing import Process
import time
import re
import RPi.GPIO as GPIO          
from time import sleep
import json

#{1234,7621}


#print("\n")
#print("The default speed & direction of motor is LOW & Forward.....")
#print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
#print("\n")





def main():
    #versturen
    def input_and_send():
        print("\nType something\n")
        while True:
            #data = input()
            #if len(data) == 0: break
            data = 1
            # time.sleep(40)
            sock.send("ahoi")
            sock.send("\n")
    #ontvangen        
    def rx_and_echo():
        in1 = 6
        in2 = 5
        in3 = 13
        in4 = 26
        ena = 25
        enb = 12
        temp1=1
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(in3,GPIO.OUT)
        GPIO.setup(in4,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        GPIO.setup(enb,GPIO.OUT)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        pa=GPIO.PWM(ena,1000)
        pb=GPIO.PWM(enb,1000)
        pa.start(25)
        pb.start(25)
        
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sock.send("\nsend anything\n")
                
        ly = 0
        lx = 0
        ry = 0
        rx = 0
    
        while True:
            data = sock.recv(buf_size)

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
            
            #print(lx)
        
            print("New values are %s %s %s %s" % (ly, lx, ry, rx))
            
            #pa.ChangeDutyCycle(50)
            #time.sleep(3)
            
            if rx < 1500 and rx > 1000:
                print("rx < 1000")
                #changeMotorSpeed(50)
                pa.ChangeDutyCycle(25)
            elif rx < 1000 and rx > 500:
                pa.ChangeDutyCycle(50)
            elif rx < 500:
                pa.ChangeDutyCycle(100)
            elif rx >= 1000:
                print("rx >= 1000")
                #changeMotorSpeed(25)
                pa.ChangeDutyCycle(0)
            
    #MAC address of ESP32
    addr = "84:CC:A8:69:97:D2"
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    #service_matches = find_service( uuid = uuid, address = addr )
    service_matches = find_service( address = addr )

    buf_size = 64;

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
    sock=BluetoothSocket(RFCOMM)
    sock.connect((host, port))

    print("connected")
    
    #time.sleep(2)
    #pa.ChangeDutyCycle(50)
    

    
    def changeMotorSpeed(speed):
        print("Set speed to %s", speed)
        pa.ChangeDutyCycle(speed)
    
    #changeMotorSpeed()
    #pa.ChangeDutyCycle(25)
    #pa.ChangeDutyCycle(50)
    #pa.ChangeDutyCycle(15)
    
    proc1 = Process(target=input_and_send)
    proc1.start()

    proc2 = Process(target=rx_and_echo)
    proc2.start()

    #proc3 = Process(target=changeMotorSpeed, args=(pa))
    #proc3.start()
    
    #input_and_send()
    #rx_and_echo()

    #sock.close()
    #print("\n--- bye ---\n")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted, shutting down program")
        pa.stop()
        sock.close()
        sys.exit(0)
        pass