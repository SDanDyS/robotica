#!/usr/bin/python

import smbus
import time
bus = smbus.SMBus(1)
address = 0x8
while True:
    data = ""
    for i in range(0, 3):
        try:
            data += chr(bus.read_byte(address))
        except:
            print("No data")
            continue
    print(data)
    time.sleep(1)