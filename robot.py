from vision.robotVision import *
from threading import *

robot = robotVision()

#INVOKE THE THREAD. UPON PRESSING Q THE THREAD WILL TERMINATE.
#CREATE SOME SORT OF HANDLER IN CASE THE THREAD SHOULD START AGAIN
robot.FLAG = 1
robot.start()