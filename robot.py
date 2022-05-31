import argparse
from vision.robotVision import *
from threading import *
from weight.example import *

# Grab arguments from Python command
# 'pi' grabs PiCamera, 0-9 grabs regular webcam camera. Defaults to 'pi'.
# ap = argparse.ArgumentParser()
# ap.add_argument("-cam", "--camera", type=str, required=True,
#                 help='Enter \'pi\' for Raspberry Pi cam, 0-9 for regular webcam connection. Defaults to Pi.')
# args = vars(ap.parse_args())

# vision = robotVision()
# 
# # INVOKE THE THREAD. UPON PRESSING Q THE THREAD WILL TERMINATE.
# # CREATE SOME SORT OF HANDLER IN CASE THE THREAD SHOULD START AGAIN
# vision.camSelector = args["camera"]
# vision.FLAG = 1
# vision.start()
weight = Weight()
weight.start()