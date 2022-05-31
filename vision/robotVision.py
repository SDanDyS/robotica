import math
from cv2 import findContours
from distance.afstandsensor import *
import numpy as np
import cv2 as cv
from threading import *
import os
import time

try:
    from imutils.video.pivideostream import PiVideoStream
    import imutils
except ImportError:
    print("Couldn't import PiCamera, continuing wihout...")


class robotVision(Thread):
    def run(self):
        self.lower_blue = np.array([90, 50, 70])
        self.upper_blue = np.array([128, 255, 255])
        self.lower_white = np.array([0,0,0], dtype=np.uint8)
        self.upper_white = np.array([0,0,255], dtype=np.uint8)
        self.absoluteDistance = []
        self.i = 0

        self.camIsPi = False

        # Check whether cam arg is Pi camera
        if self.camSelector == "pi":
            print("Selecting PiCamera")
            self.camIsPi = True

            resW = 320
            resH = 320
            resolution = (resW, resH)
            self.screenWidth = resW
            self.screenHeight = resH

            rotation = 90
            vs = PiVideoStream(resolution=resolution, rotation=rotation).start()
            time.sleep(1)
        # Otherwise select USB camera
        elif self.camSelector.isnumeric():
            print("Selecting regular USB camera")
            self.camIsPi = False
            self.cap = cv.VideoCapture(int(self.camSelector))

            if not self.cap.isOpened():
                print("Cannot open camera")
                exit()
            self.screenWidth = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
            self.screenHeight = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`

        while True:
            # Capture frame-by-frame
            if self.camIsPi == True:
                self.frame = vs.read()
                #frame = imutils.resize(frame, width=400)
            else:
                self.ret, self.frame = self.cap.read()

                # if frame is read correctly ret is True
                if not self.ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

            cv.circle(self.frame, (int(self.screenWidth / 2), int(self.screenHeight / 2)), 5, (255, 255, 255), -1)

            blur = cv.GaussianBlur(self.frame, (37, 37), 0)
            self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
            #distance and width
            self.getFocalLength(self.screenWidth, 20, 21)

            # #FLAG 1 REPRESENTS DETECTING COOKIES
            # #FLAG 2 REPRESENTS SIMPLY DETECING A MOVING OBJECT
            if (self.FLAG == 1):
                self.distance = sensorDistance()
                
                if (self.i == 0):
                    while (self.i < 5):
                        freq = str(self.distance).split(".")
                        self.absoluteDistance.append(freq[0])
                        self.i += 1
                else:
                    freq = str(self.distance).split(".")
                    distanceConfirmed = calibrate_distance(self.absoluteDistance, len(self.absoluteDistance))
                    
                    self.i = 0
                    self.absoluteDistance = []
                    
                    if ((int(freq[0]) + 1) != int(distanceConfirmed) and (int(freq[0]) - 1) != int(distanceConfirmed) and (int(freq[0])) != int(distanceConfirmed)):
                        continue
                    
                    if (self.distance > 10):
                        angle = self.detectObject(self.lower_blue, self.upper_blue)
                        #X movement based on angle
                        # Z forward movement -> provide the distance and...
                        ## internally wietze and chris will handle the speed
                        if (angle == 0):
                            #ONLY Z FORWARD -> provide the distance and...
                            ## internally wietze and chris will handle the speed
                            pass
                    elif (self.distance <= 10):
                        armAngle = self.detectObject(self.lower_blue, self.upper_blue, True)
                        if (armAngle == 0):
                            #ARM SHOULD GO STRAIGHT DOWN
                            ##gripperMethod(armAngle)
                            #to change the gripper and bring it up and down. Due to knowing the angle, we can rotate the negative to positive
                            #and vice versa
                            #example : 10 degrees angle, so after finish we do -10 passed to the gripper
                            # -10 degrees angle, so after finish we do 10 passed to the gripper
                            pass
            elif (self.FLAG == 2):
                angle = self.detectObject(self.lower_blue, self.upper_blue, forcedDistance=200)
                #PASS ANGLE TO wietze AND chris, they handle the speed Y
                #ONLY Y FORWARD BACKWARD BASED ON ANGLE

            self.imshow()

            if cv.waitKey(1) == ord('q'):
                self.releaseStream()
                GPIO.cleanup()
                break

    def detectObject(self, lower, upper, gripper = False, forcedDistance = False):
        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(self.hsv, lower, upper)
        print(gripper)
        cnts = self.findContours(mask)
        if (len(cnts) > 0):
            # return the biggest contourArea and determine centroid
            area = max(cnts, key=cv.contourArea)
            self.centroid(area)
            (xg, yg, wg, hg) = cv.boundingRect(area)
            cv.rectangle(self.frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

            # WE ARE NOT ACTUALLY CALCULATING WIDTH OF THE OBJECT, BUT RATHER POINT 0 TO POINT CENTROID X
            rCM = 0
            if (forcedDistance):
                if (forcedDistance != 0):
                    objW = self.pointZeroToObjectCentroid(self.cx(area), forcedDistance, self.focalLength)
                    screenW = self.pointZeroToObjectCentroid(int(self.screenWidth / 2), forcedDistance, self.focalLength)
                    rCM = objW - screenW                
            elif (self.distance != 0 and self.distance < 199):
                distanceToCamera = self.getCameraDistance(self.distance, 12)
                objW = self.pointZeroToObjectCentroid(self.cx(area), distanceToCamera, self.focalLength)
                screenCentroid = self.pointZeroToObjectCentroid(int(self.screenWidth / 2), distanceToCamera, self.focalLength)
                rCM = objW - screenCentroid

            # either no object was detected to determine width or the threshold has been hit and therefore...
            # no position has to change
            if (rCM != 0):
                if (gripper is False):
                    if (rCM > 0.5 or rCM < -0.5):
                        atan = self.angle_atan(self.distance, rCM)
                        return atan
                else:
                    atan = self.angle_atan(self.distance, rCM)
                    return atan
            return 0

    def centroid(self, momentsToCalculate, draw=True):
        m = cv.moments(momentsToCalculate)
        if ((m['m10'] and m['m00']) and (m['m01'] and m['m00'])):
            # calculate centroid of mass and draw it
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            if (draw):
                cv.circle(self.frame, (cx, cy), 5, (255, 255, 255), -1)
        # return for external use
        return m

    def cx(self, momentsToCalculate):
        m = cv.moments(momentsToCalculate)
        cx = 0
        if ((m['m10'] and m['m00'])):
            # calculate centroid of mass for x axis
            cx = int(m['m10']/m['m00'])
        return cx

    def cy(self, momentsToCalculate):
        m = cv.moments(momentsToCalculate)
        cy = 0
        if ((m['m01'] and m['m00'])):
            # calculate centroid of mass and draw it
            cy = int(m['m01']/m['m00'])
        return cy

    def releaseStream(self):
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

    def imshow(self):
        cv.imshow("Video capture (Final result)", self.frame)

    def findContours(self, mask):
        return cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

    # Calculate the focal length of the camera
    def getFocalLength(self, pixelWidth, distance, width):
        self.focalLength = (pixelWidth * distance) / width

    def pointZeroToObjectCentroid(self, pixel, distance, focal):
        w = (pixel * distance) / focal
        return w

    # Get the distance from the camera to the object from the distance from the sensor to the object and the hight of the camera
    def getCameraDistance(self, distanceToObject, heightToCamera):
        cameraDistance = distanceToObject**2 + heightToCamera**2
        return math.sqrt(cameraDistance)

    #this returns the value in degrees! INVERSES THE TAN !
    def angle_atan(self, adjacentSide, oppositeSide):
        value = oppositeSide / adjacentSide
        return math.degrees(math.atan(value))