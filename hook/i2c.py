#  Raspberry Pi Master for Arduino Slave
#  i2c_master_pi.py
#  Connects to Arduino via I2C
  
#  DroneBot Workshop 2019
#  https://dronebotworkshop.com

from smbus import SMBus
from threading import *

class i2c(Thread):
		addr = 0x8 # bus address
		bus = SMBus(1) # indicates /dev/ic2-1
		numb = 1

		# Stops the height servos
		def stopHeight(self):
				self.bus.write_byte(addr, 0x0)

		# Arm goes up
		def raiseHeight(self):
				self.bus.write_byte(addr, 0x1)

		# Arm goes down
		def lowerHeight(self):
				self.bus.write_byte(addr, 0x2)

		# Opens the grabber
		def openGrabber(self):
				self.bus.write_byte(addr, 0x3)

		def closeGrabber(self):
				self.bus.write_byte(addr, 0x4)

		def stopGrabber(self):
				self.bus.write_byte(addr, 0x5)

		def controlArm(self, input):
				# Stop height servos
				if ledstate == "0":
						self.stopHeight()
				# Arm goes up
				elif ledstate == "1":
						self.raiseHeight()
				# Arm goes down
				elif ledstate == "2":
						self.lowerHeight()
				# Open the grabber
				elif ledstate == "3":
						self.openGrabber()
				# Close the grabber
				elif ledstate == "4":
						self.closeGrabber()
				# Stop the grabber servo
				elif ledstate == "5":
						self.stopGrabber()

		def consoleInterface(self):
				print ("Enter 1 for ON or 0 for OFF")
				while self.numb == 1:

					ledstate = input(">>>>   ")

					if ledstate == "1":
						self.bus.write_byte(addr, 0x1)
					if ledstate == "2":
						self.bus.write_byte(addr, 0x2)# switch it on
					# switch it on
					if ledstate == "3":
						self.bus.write_byte(addr, 0x3)
					if ledstate == "4":
						self.bus.write_byte(addr, 0x4)
					if ledstate == "5":
						self.bus.write_byte(addr, 0x5)# switch it on# switch it on
					elif ledstate == "0":
						self.bus.write_byte(addr, 0x0) # switch it on
				