#!/usr/bin/python
import sys
import smbus
import time
bus = smbus.SMBus(1)
address = 0x8
weightList = []
while True:
    data = ""
    weightList = []
    for i in range(0, 4):
        # data += chr(bus.read_byte(address))
        data += chr(bus.read_byte(address))
        # print(chr(bus.read_byte(address)))
        # print(chr(bus.read_byte(address)))
        # print(chr(bus.read_byte(address)))
 
    data = int(data.replace(b'\x00', b''))
    # data.encode('utf-8')
    # print(data.decode('utf-8'))

    print(data)
    print(type(data))
    print(data.isnumeric())
    print(int(data))
    # data = data.encode("utf-8")
    # data = int.from_bytes(data, sys.byteorder)
    # data = int(data)+191
    # print(data)
    time.sleep(1)