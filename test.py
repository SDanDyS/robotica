import math
from cv2 import findContours
from distance.HCSRO4Component import *
from drive.dcMotorIndu import *
import numpy as np
import cv2 as cv
from threading import *
import os
import time
import logging

try:
    from imutils.video.pivideostream import PiVideoStream
    import imutils
except ImportError:
    logging.warning("Couldn't import PiCamera, continuing wihout...")
    

camIsPi = True
# Check whether cam arg is Pi camera

rotation = 90
vs = PiVideoStream(rotation=rotation).start()
time.sleep(1)

cycleOn = True
while (cycleOn == True):
    # Capture frame-by-frame
    frame = vs.read()
    print(frame)
    #frame = imutils.resize(frame, width=400)                
    cv.imshow("Video capture (Final result)", frame)
