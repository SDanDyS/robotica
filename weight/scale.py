import time
import sys
from threading import *
import RPi.GPIO as GPIO
from hx711 import HX711

referenceUnit = 1
    

class Weight(Thread):
    def run(self):
        self.hx = HX711(17, 27)
        self.hx.set_reading_format("MSB", "MSB")
        # self.hx.set_reference_unit(1)
        self.hx.reset()
        self.hx.tare()
        while True:
            try:
                # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
                val = max(0, int(self.hx.get_weight(1)))
                print(self.hx.get_weight(1) / 1000)
                self.hx.power_down()
                self.hx.power_up()
                time.sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()
        
    def cleanAndExit():
        GPIO.cleanup()
        sys.exit()

w = Weight()
w.start()