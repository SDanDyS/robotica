from bluetooth import *
from multiprocessing import Process
import time


def main():
    #versturen
    def input_and_send():
        print("\nType something\n")
        while True:
            #data = input()
            #if len(data) == 0: break
            data = 1
            
            sock.send(str(data))
            sock.send("\n")
    #ontvangen        
    def rx_and_echo():
        sock.send("\nsend anything\n")
        while True:
            data = sock.recv(buf_size)
            #if data:
            #time.sleep(0.1)
            if not data: break
            print(data)
                #sock.send(data)

    #MAC address of ESP32
    addr = "84:CC:A8:69:97:D2"
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    #service_matches = find_service( uuid = uuid, address = addr )
    service_matches = find_service( address = addr )

    buf_size = 16;

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