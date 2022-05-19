from bluetooth import *
from multiprocessing import Process
import time
import re
import RPi.GPIO as GPIO          
from time import sleep

{1234,7621}

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
        sock.send("\nsend anything\n")
        
        #pa.ChangeDutyCycle(50)
    
        while True:
            data = sock.recv(buf_size)
            #if data:
            #numeric_string = re.sub("[^0-9]","",data.decode("utf-8"))
            #print(numeric_string)
#             numeric_string2 = numeric_string[4:8]
#             numeric_string = numeric_string[0:4]
            #print("numeric_string:")
            #numeric_string = int(numeric_string)
            #print(numeric_string)
#             numeric_string2 = int(numeric_string2)
            #data = int(numeric_string[0:4])
            #data2 = int(data2)
            
            utfData = data.decode("utf-8")
            #print("utfData:")
            #print(utfData)
            
            splitValues = utfData.split(",")
            #print("splitValues:")
            #print(splitValues)
            
            ly = 0
            lx = 0
            ry = 0
            rx = 0
            
            for value in splitValues:
                # Get LY value
                try:
                    lyValue = value.split("LY", 1)
                    if lyValue[1]:
                        ly = lyValue[1]
                        #print("LY value:")
                        #print(lyValue[1])
                except:
                    pass
                
                # Get LX value
                try:
                    lxValue = value.split("LX", 1)
                    if lxValue[1]:
                        lx = lxValue[1]
                        #print("LX value:")
                        #print(lxValue[1])
                except:
                    pass
                
                # Get RY value
                try:
                    ryValue = value.split("RY", 1)
                    if ryValue[1]:
                        ry = ryValue[1]
                        #print("RY value:")
                        #print(ryValue[1])
                except:
                    pass
                
                # Get RX value
                try:
                    rxValue = value.split("RX", 1)
                    if rxValue[1]:
                        rx = rxValue[1]
                        print("RX value:")
                        print(rxValue[1])
                        
                        if int(rx) < 1000:
                            print("joystick moved")
                            pa.ChangeDutyCycle(50)
                        elif int(rx) > 1000:
                            print("no movement")
                            pa.ChangeDutyCycle(25)
                except:
                    pass
            #print("New values are %s %s %s %s" % (ly, lx, ry, rx))

        
            # exec
            #if rx:
#             print("int(rx):")
#             print(int(rx))
#             if int(rx) < 1000:
#                 pa.ChangeDutyCycle(75)
#             elif int(rx) > 1000:
#                 pa.ChangeDutyCycle(10)
# 
            #(numeric_string)
            #print(numeric_string2)
            #data1 = data[1:2]
            #data2 = numeric_string[4:8]
            #data3 = numeric_string[8:12]
            #data4 = numeric_string[12:16]
#           data3 = int(data3)
            #print(type(
#             #print(numeric_string)
#             if numeric_string > 1000:
#                 #print(numeric_string)
#                 
#     
#                 
#                 
                #print("run")
#                 if(temp1==1):
#                     GPIO.output(in1,GPIO.HIGH)
#                     GPIO.output(in2,GPIO.LOW)
#                     
#                     #print("forward")
#                     x='z'
#                 elif numeric_string > 1200:
#                     #print("medium")
#                     pa.ChangeDutyCycle(50)
#                 elif  numeric_string> 9:
#                     GPIO.cleanup()
#                     break
                    
            if not data: break
            #print(data)
            #if data2 > 1840:
            #print(numeric_string)
            #x
#             print(data)
#             print(data2)
#             #y
#             print(data3)
#             print(data4)
                #sock.send(data)

    #MAC address of ESP32
    addr = "84:CC:A8:69:97:D2"
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    #service_matches = find_service( uuid = uuid, address = addr )
    service_matches = find_service( address = addr )

    buf_size = 32;

    if len(service_matches) == 0:
        print("couldn't find the SampleServer service =(")
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
    
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

    proc1 = Process(target=input_and_send)
    proc1.start()

    proc2 = Process(target=rx_and_echo)
    proc2.start()

    
    #input_and_send()
    #rx_and_echo()

    #sock.close()
    #print("\n--- bye ---\n")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted, shutting down program")
        sock.close()
        sys.exit(0)
        pass