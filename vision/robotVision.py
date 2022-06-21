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
        self.areaIsNone = []
        self.start_parkour = True

        motor_left = dcMotorIndu(0)
        motor_right = dcMotorIndu(1)

        self.camIsPi = False

        # Check whether cam arg is Pi camera
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

            cv.circle(self.frame, (int(self.screenWidth / 2), int(self.screenHeight / 2)), 5, (255, 255, 255), -1)
            #distance and width
            self.getFocalLength(self.screenWidth, 20, 15)

            # #FLAG 1 REPRESENTS DETECTING COOKIES
            # #FLAG 2 REPRESENTS SIMPLY DETECING A MOVING OBJECT
            # FLAG 3 REPRESENTS GOING UP THE PARCOUR
            if (self.FLAG == 1):
                #FORCE A TIME SLEEP TO PREVENT CPU FROM CRASHING
                time.sleep(1)
                self.distance = sensorDistance()
                blur = cv.GaussianBlur(self.frame, (37, 37), 0)
                self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

                # ENFORCE A CALIBRATED DISTANCE
                if (self.i < 5):
                    freq = str(self.distance).split(".")
                    self.absoluteDistance.append(freq[0])
                    self.i += 1
                else:
                    freq = str(self.distance).split(".")
                    distanceConfirmed = max_frequency(self.absoluteDistance, len(self.absoluteDistance))
                    
                    self.i = 0
                    self.absoluteDistance = []
                    
                    if ((int(freq[0]) + 1) != int(distanceConfirmed) and (int(freq[0]) - 1) != int(distanceConfirmed) and (int(freq[0])) != int(distanceConfirmed)):
                        pass
                    elif (self.distance > 10 and self.distance <= 199):
                        area = self.detectObject(self.lower_blue, self.upper_blue)
                        # NO OBJECT ON CAM, BUT DISTANCE CALCULATED SOME OBJECT
                        if (area is None and self.distance <= 199):
                            if (self.distance > 76):
                                self.motor_left.forward(100)
                                self.motor_right.forward(100)
                                time.sleep(1)
                                self.motor_left.stop()
                                self.motor_right.stop()        
                            else:
                                pass
                                #NO OBJECT WAS DETECTED BUT IT SHOULDVE BEEN IN RANGE
                                #THEREFORE WE CAN SAY THE OBJECT IS A FALSE POSITIVE
                                #START DOING SOME RNG MOVEMENT AS IF IT'S LOOKING FOR OBJECTS

                        elif (area is not None):
                            self.drawDetectedObject(area)
                            if (self.distance >= 40):
                                angle = self.angleToRotate(area, self.distance)
                                if (angle <= -9):
                                    motor_left.backwards(10)
                                    motor_right.forward(10)
                                elif (angle is not None and angle >= 9):
                                    motor_left.forward(10)
                                    motor_right.backwards(10)

                                time.sleep(1)
                                motor_left.stop()
                                motor_right.stop()
                                time.sleep(0.1) 
                                motor_left.forward(100)
                                motor_right.forward(100)
                                time.sleep(0.5)       
                                motor_left.stop()
                                motor_right.stop()
                            elif (self.distance >= 30):
                                angle = self.angleToRotate(area, self.distance)
                                if (angle <= -9):
                                    motor_left.backwards(10)
                                    motor_right.forward(10)
                                elif (angle is not None and angle >= 9):
                                    motor_left.forward(10)
                                    motor_right.backwards(10)
                            
                                time.sleep(1)
                                motor_left.stop()
                                motor_right.stop()
                                time.sleep(0.1) 
                                motor_left.forward(15)
                                motor_right.forward(15)
                                time.sleep(0.5)       
                                motor_left.stop()
                                motor_right.stop()
                            else:
                                #CHECK YOUR PHOTO GALLERY FOR IMPLEMENTATION DANIEL
                            












                            # self.drawDetectedObject(area)
                            # angle = self.angleToRotate(area)
                            #DO SOME RNG FORWARD, LEFT/RIGHT, BACKWARD MOVEMENT
                            #AS IF IT'S SCANNING FOR SOMETHING
                            pass
                        elif (angle is None and self.distance < 199):
                            if (self.distance >= 76):
                                motor_left.forward(100)
                                motor_right.forward(100)
                                time.sleep(1)
                                motor_left.stop()
                                motor_right.stop()
                        elif (angle > 0):
                            motor_left.forward(25)
                            motor_right.backwards(25)
                        elif (angle < 0):
                            motor_left.backwards(25)
                            motor_right.forward(25)

                        time.sleep(0.5)
                        motor_left.forward(50)
                        motor_right.forward(50)
                        time.sleep(1)
                        motor_left.stop()
                        motor_right.stop()
            elif (self.FLAG == 2):
                blur = cv.GaussianBlur(self.frame, (9, 9), 0)
                self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
                area = self.detectObject(self.lower_blue, self.upper_blue)
                if (area is not None):
                    self.drawDetectedObject(area)
                    angle = self.angleToRotate(area, 200)
                    if (angle is not None and angle < -1):
                        motor_left.backwards()
                        motor_right.backwards()
                    elif (angle is not None and angle > 1):
                        motor_left.forward(100)
                        motor_right.forward(100)
            elif (self.FLAG == 3):
                if (start_parkour == True):
                    motor_left.forward(100)
                    motor_right.forward(100)
                    time.sleep(3)
                    motor_left.stop()
                    motor_right.stop()
                    start_parkour = False
                blur = cv.GaussianBlur(self.frame, (9, 9), 0)
                # self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
                # self.areaIsNone = 0

                # area = self.detectObject(lower_val, upper_val)

                hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
                            
                # # define range of black color in HSV
                # lower_val = np.array([0,0,0])
                # upper_val = np.array([179,100,30])
                # # Threshold the HSV image to get only black colors
                # mask = cv.inRange(hsv, lower_val, upper_val)

                # red mask
                lower_red = np.array([0,50,50])
                upper_red = np.array([10,255,255])

                red_mask_low = cv2.inRange(hsv, lower_red, upper_red)

                # red mask
                lower_red = np.array([170,50,50])
                upper_red = np.array([180,255,255])

                red_mask_upper = cv2.inRange(hsv, lower_red, upper_red)

                mask = red_mask_low | red_mask_upper

                cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
                abscnts = []
                if (len(cnts) > 0):
                    for cnt in cnts:
                        if (self.isBadContour(cnt) == False):
                            abscnts.append(cnt)
                    area = max(cnts, key=cv.contourArea)
                    (xg, yg, wg, hg) = cv.boundingRect(area)
                    cv.rectangle(self.frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

                    if (area is not None):
                        self.drawDetectedObject(area)
                        angle = self.angleToRotate(area, 25,  offset=-6.1) ##MAYBE REMOVE OFFSET, JUST SET THE CAMERA IN ONE LINE WITH THE LINE-TO-FOLLOW
                        if (angle is not None and angle <= -9):
                            motor_left.backwards(6)#11 SHOULD BE 10, BUT THEORY CAN BE DIFFERENT FROM REAL. CHANGE BACK TO 10 IF 11 IS TOO MUCH
                            motor_right.forward(6)
                        elif (angle is not None and angle >= 9):
                            motor_left.forward(6)
                            motor_right.backwards(6)

                        time.sleep(1)       
                        motor_left.stop()
                        motor_right.stop()
                        time.sleep(0.5)
                        motor_left.forward()
                        motor_right.forward()                        
                # elif (area is None):
                #     print()
                #     #cycle 3 times, upon 3 times area is none do a 180 degrees flip on robot
                #     if (self.areaIsNone > 4):
                #         motor_left.backwards()
                #         motor_right.forward()
                #         time.sleep(2)
                #         motor_left.stop()
                #         motor_right.stop()
                #         time.sleep(0.5)
                #         print("ENGAGED")
                #         # self.gaugeAndCrawl()
                #     else:
                #         self.areaIsNone += 1

            self.imshow()
            # global stop_vision_thread
            if cv.waitKey(1) == ord('q'):
                # When everything done, release the capture
                self.cycleOn = False
                GPIO.cleanup()
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
    def angleToRotate(self, area, forcedDistance = False, offset = False):
            # WE ARE NOT ACTUALLY CALCULATING WIDTH OF THE OBJECT, BUT RATHER POINT 0 TO POINT CENTROID X
            rCM = 0
            if (forcedDistance):
                self.distance = forcedDistance
                if (forcedDistance != 0):
                    objW = self.pointZeroToObjectCentroid(self.cx(area), forcedDistance, self.focalLength)
                    screenW = self.pointZeroToObjectCentroid(int(self.screenWidth / 2), forcedDistance, self.focalLength)
                    rCM = objW - screenW                
            elif (self.distance != 0 and self.distance < 199):
                distanceToCamera = self.getCameraDistance(self.distance, 25)
                objW = self.pointZeroToObjectCentroid(self.cx(area), distanceToCamera, self.focalLength)
                screenCentroid = self.pointZeroToObjectCentroid(int(self.screenWidth / 2), distanceToCamera, self.focalLength)
                if (offset is not False):
                    rCM = objW - (screenCentroid + offset)
                else:
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