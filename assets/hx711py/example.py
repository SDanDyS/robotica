import time
import sys
from threading import *
import RPi.GPIO as GPIO
from hx711 import HX711

referenceUnit = 1
    

class Weight(Thread):
    def run(self):
        hx = HX711(5, 6)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(-441)
        hx.reset()
        hx.tare()
        print("Tare done! Add weight now...")
        while True:
            try:
                # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
                val = max(0, int(hx.get_weight(5)))
                print(val)
                hx.power_down()
                hx.power_up()
                time.sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()