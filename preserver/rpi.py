# !/bin/python
import RPi.GPIO as GPIO
import time
import os
import threading


##https://forums.raspberrypi.com/viewtopic.php?t=236338
# Use the Broadcom SOC Pin numbers
# Setup the pin with internal pullups enabled and pin in reading mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Shutdown function
def shutdown(channel):
    os.system("sudo shutdown -h now")

# Add our function to execute 
GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdown, bouncetime=2000)

"""
    sudo crontab -e
    @reboot                           
"""