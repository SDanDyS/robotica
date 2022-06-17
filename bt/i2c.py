#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C

#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

from smbus import SMBus
from threading import *
import time
import sys
import re


WEIGHT_ARM = 185

class i2c(Thread):
    weight = 0
    voltage = 0

    def run(self):
        self.addr = 0x8  # bus address
        self.bus = SMBus(1)  # indicates /dev/ic2-1
        self.numb = 1
        self.receiveData()

    def receiveData(self):
        while True:
            data = ""
            for i in range(0, 9):
                try:
                    data += chr(self.bus.read_byte(self.addr))
                except Exception as e:
                    print(e)

            '''
            i2c not connected: ['\x00\x00\x00\x00\x00\x00\x00\x00\x00']
            '''

            # TODO: replace with actual `data`
            data = "800@700"

            if "@" in data:
                splitData = data.split("@", 1)
                # Set correct values
                weightData = splitData[0]
                voltageData = splitData[1]

                # Clean up '\x00'
                weightData = weightData.replace('\x00', '')
                voltageData = voltageData.replace('\x00', '')
                # print("weightData:")
                # print(weightData)
                # print("voltageData:")
                # print(voltageData)

                self.weight = int(weightData)
                self.voltage = int(voltageData)
            else:
                print("Received invalid data from i2c")

            time.sleep(0.3)

    def getWeight(self):
        # if self.weight == 0:
        #     return 0
        return (self.weight - WEIGHT_ARM)
    
    def getVoltage(self):
        # 735/12.6
        return self.voltage / 58.3

    # Stops the height servos
    def stopHeight(self):
        self.bus.write_byte(self.addr, 0x0)

    # Arm goes up
    def raiseHeight(self):
        self.bus.write_byte(self.addr, 0x1)

    # Arm goes down
    def lowerHeight(self):
        self.bus.write_byte(self.addr, 0x2)

    # Opens the grabber
    def openGrabber(self):
        self.bus.write_byte(self.addr, 0x3)

    def closeGrabber(self):
        self.bus.write_byte(self.addr, 0x4)

    def stopGrabber(self):
        self.bus.write_byte(self.addr, 0x5)

    def controlArm(self, input):
        # Stop height servos
        if input == "0":
            self.stopHeight()
        # Arm goes up
        elif input == "1":
            self.raiseHeight()
        # Arm goes down
        elif input == "2":
            self.lowerHeight()
        # Open the grabber
        elif input == "3":
            self.openGrabber()
        # Close the grabber
        elif input == "4":
            self.closeGrabber()
        # Stop the grabber servo
        elif input == "5":
            self.stopGrabber()

    def consoleInterface(self):
        print("Enter 1 for ON or 0 for OFF")
        while self.numb == 1:

            ledstate = input(">>>>   ")

            if ledstate == "1":
                self.bus.write_byte(self.addr, 0x1)
            if ledstate == "2":
                self.bus.write_byte(self.addr, 0x2)
            if ledstate == "3":
                self.bus.write_byte(self.addr, 0x3)
            if ledstate == "4":
                self.bus.write_byte(self.addr, 0x4)
            if ledstate == "5":
                self.bus.write_byte(self.addr, 0x5)
            elif ledstate == "0":
                self.bus.write_byte(self.addr, 0x0)
