from vision.robotVision import *
from threading import *

robot = robotVision()

# INVOKE THE THREAD. UPON PRESSING Q THE THREAD WILL TERMINATE.
# CREATE SOME SORT OF HANDLER IN CASE THE THREAD SHOULD START AGAIN
robot.FLAG = 2
robot.start()
# robot.getFocalLength(248, 11, 24)
robot.getFocalLength()
print("Distance: " + str(robot.getDistance(800)))
