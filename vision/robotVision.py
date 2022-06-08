import math
from queue import Empty
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

"""
    RobotVision class holds all the vision related data
"""
class RobotVision(Thread):
    """
        Entry point of the start method
        Initializes all the required data
        Serves as a controller for the rest of the class
    """
    def run(self):
        self.lower_blue = np.array([90, 50, 70])
        self.upper_blue = np.array([128, 255, 255])
        self.absoluteDistance = []
        self.i = 0
        self.cycleOn = True

        motor_left = dcMotorIndu(0)
        motor_right = dcMotorIndu(1)

        self.camIsPi = False

        # Check whether cam arg is Pi camera
        if self.camSelector == "pi":
            logging.info("Selecting PiCamera")
            self.camIsPi = True

            resW = 320
            resH = 320
            resolution = (resW, resH)
            self.screenWidth = resW
            self.screenHeight = resH

            rotation = 90
            vs = PiVideoStream(resolution=resolution, rotation=rotation).start()
            time.sleep(1)
        
        while (self.cycleOn == True):
            # Capture frame-by-frame
            if self.camIsPi == True:
                self.frame = vs.read()
                #frame = imutils.resize(frame, width=400)

            cv.circle(self.frame, (int(self.screenWidth / 2), int(self.screenHeight / 2)), 5, (255, 255, 255), -1)
            cv.circle(self.frame, (int(self.screenWidth / 2), int(self.screenHeight / 2 - 75)), 5, (255, 255, 255), -1)
            cv.circle(self.frame, (int(self.screenWidth / 2), int(self.screenHeight / 2 + 75)), 5, (255, 255, 255), -1)
            #distance and width
            self.getFocalLength(self.screenWidth, 20, 15)

            # #FLAG 1 REPRESENTS DETECTING COOKIES
            # #FLAG 2 REPRESENTS SIMPLY DETECING A MOVING OBJECT
            if (self.FLAG == 1):
                self.distance = sensorDistance()

                blur = cv.GaussianBlur(self.frame, (37, 37), 0)
                self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

                # ENFORCE A CALIBRATED DISTANCE
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
                        pass
                    elif (self.distance > 10):
                        area = self.detectObject(self.lower_blue, self.upper_blue)
                        self.drawDetectedObject(area)
                        angle = self.angleToRotate(area)
                        # NO CONTOUR FOUND AND THEREFORE NO OBJECT FOUND
                        if (angle is None):
                            #DO SOME RNG FORWARD, LEFT/RIGHT, BACKWARD MOVEMENT
                            #AS IF IT'S SCANNING FOR SOMETHING
                            pass
                        elif (angle > 0):
                            motor_left.left()
                            motor_right.right()
                        elif (angle < 0):
                            motor_left.right()
                            motor_right.left()

                        motor_left.forward(100)
                        motor_right.forward(100)
                        time.sleep(1)
                        motor_left.stop()
                        motor_right.stop()
                        #SOMETHING WAS MEASURED, BUT NO VISION ON TARGET
                    elif (self.distance <= 10):
                        area = self.detectObject(self.lower_blue, self.upper_blue)
                        self.drawDetectedObject(area)
                        angle = self.angleToRotate(area)
                        if (angle is None):
                            pass
                        else:
                            ##gripperMethod()
                            pass
            elif (self.FLAG == 2):
                blur = cv.GaussianBlur(self.frame, (9, 9), 0)#self.frame
                self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)#blur
                # int(self.screenHeight / 2 - 50), int(self.screenHeight / 2 + 50)
                area = self.detectObject(self.lower_blue, self.upper_blue, int(self.screenHeight / 2 - 75), int(self.screenHeight / 2 + 75))
                if (area is not None):
                    self.drawDetectedObject(area)
                    angle = self.angleToRotate(area, 200)
                    if (angle is not None and angle < -1):
                        motor_left.backwards()
                        motor_right.backwards()
                    elif (angle is not None and angle > 1):
                        motor_left.forward(100)
                        motor_right.forward(100)

            self.imshow()
            if cv.waitKey(1) == ord('q'):
                # When everything done, release the capture
                self.cycleOn = False
                GPIO.cleanup()
                cap.release()
                cv.destroyAllWindows()
                break

    """
        Draws a rectangle based on  provided area and prints centroid
    """
    def drawDetectedObject(self, area):
        self.centroid(area)
        (xg, yg, wg, hg) = cv.boundingRect(area)
        cv.rectangle(self.frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

    """
        Provide area and optionally a forcedDistance
        Based on distance and camera it determines how many degrees the object has to turn
    """
    def angleToRotate(self, area, forcedDistance = False):
            # WE ARE NOT ACTUALLY CALCULATING WIDTH OF THE OBJECT, BUT RATHER POINT 0 TO POINT CENTROID X
            rCM = 0
            if (forcedDistance):
                self.distance = forcedDistance
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
                if (rCM > 0.5 or rCM < -0.5):
                    atan = self.angleAtan(self.distance, rCM)
                    return atan
            #NO ROTATION REQUIRED
            return 0

    """
        Accept a contour and determine whether it's a rectangle or not
    """
    def isBadContour(self, c):
        # approximate the contour
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        # the contour is 'bad' if it is not a rectangle
        return not len(approx) == 4

    """
        Detect objects based on a mask (HSV) value
        Optionally a top value of pixels and bottom value of pixels can be provided to narrow the search scope
    """
    def detectObject(self, lower, upper, topVal = False, botVal = False):
        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(self.hsv, lower, upper)
        cnts = self.findContours(mask)
        filtercnts = []
        cntArea = None
        #contours were found
        if (len(cnts) > 0):
            ##topval is min, botval is pos
            if (botVal is not False and topVal is not False):
                for cnt in cnts:
                    if (self.isBadContour(cnt) == False):
                        cy = self.cy(cnt)
                        if (cy > topVal and cy < botVal):
                            filtercnts.append(cnt)
                if (len(filtercnts) > 0):
                    cntArea = max(filtercnts, key=cv.contourArea)
            else:
                cntArea = max(cnts, key=cv.contourArea)

        # return the biggest contourArea
        return cntArea


    """
        Determine centroid and draw per default
        Return moments for further usage
    """
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

    """
        Calculates moments on the X axis and returns it
    """
    def cx(self, momentsToCalculate):
        m = cv.moments(momentsToCalculate)
        cx = 0
        if ((m['m10'] and m['m00'])):
            # calculate centroid of mass for x axis
            cx = int(m['m10']/m['m00'])
        return cx

    """
        Calculates moments on the Y axis and returns it
    """
    def cy(self, momentsToCalculate):
        m = cv.moments(momentsToCalculate)
        cy = 0
        if ((m['m01'] and m['m00'])):
            # calculate centroid of mass and draw it
            cy = int(m['m01']/m['m00'])
        return cy

    """
        Shows the generated frame from the RobotVision class
    """
    def imshow(self):
        cv.imshow("Video capture (Final result)", self.frame)

    """
        Find the contours based on a provided mask
        Returns ONLY the contours! Not the hierarchy!
    """
    def findContours(self, mask):
        return cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

    """
        Calculate the focal length of the camera based on a pixelWidth, distance and width
    """
    def getFocalLength(self, pixelWidth, distance, width):
        self.focalLength = (pixelWidth * distance) / width

    """
        Determine what the distance is from point A to centroid point
        Returns the distance
    """
    def pointZeroToObjectCentroid(self, pixel, distance, focal):
        w = (pixel * distance) / focal
        return w

    """
        Provide distance to object and height to the camera
        Calculates and returns the square root of C^2 = A^2 + B^2
        NOTICE: PROVIDE AN ANGLE OF 90 DEGREES! THIS IS A REQUIREMENT TO IMPLEMENT THE PYTHAGOREAN THEOREM!
    """
    def getCameraDistance(self, distanceToObject, heightToCamera):
        cameraDistance = distanceToObject**2 + heightToCamera**2
        return math.sqrt(cameraDistance)

    """
        Returns the value in degrees
        Inverses the TAN
    """
    def angleAtan(self, adjacentSide, oppositeSide):
        value = oppositeSide / adjacentSide
        return math.degrees(math.atan(value))