import math
from cv2 import findContours
import numpy as np
import cv2 as cv
from threading import *
import os
import time

class robotVision(Thread):
    # The width of the object
    WIDTH_OBJECT = 7.5
    # The distance to the object in the KNOWN_IMAGE
    KNOWN_DISTANCE = 40
    # The image that is known to be KNOWN_DISTANCE away
    KNOWN_IMAGE = 'assets/images/40cm.jpg'

    focalLength = 0

    def run(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            self.ret, self.frame = self.cap.read()

            # if frame is read correctly ret is True
            if not self.ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            self.screenWidth  = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
            self.screenHeight = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`

            gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            ret,thresh = cv.threshold(gray,127,255,0)
  
            #57 breedte
            #50 afstand
            #640 pixel width
            # self.centroid(thresh)

            blur = cv.GaussianBlur(self.frame, (37, 37), 0)
            self.hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
            self.getFocalLength(self.screenWidth, 50, 57)

            if (self.FLAG == 1):
                self.detectCookie()
            else:
                self.detectMovingObject()

            self.imshow()

            if cv.waitKey(1) == ord('q'):
                self.releaseStream()
                break

    def detectMovingObject(self):
        # define range of blue color in HSV
        #[[128, 255, 255], [90, 50, 70]]
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(self.hsv, lower_blue, upper_blue)

        bluecnts = self.findContours(mask)
        if (len(bluecnts) > 0):
            # return the biggest contourArea and determine centroid
            blue_area = max(bluecnts, key=cv.contourArea)
            self.centroid(blue_area)

            (xg, yg, wg, hg) = cv.boundingRect(blue_area)
            cv.rectangle(self.frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)
            self.widthToCm(self.cx(blue_area), 20, self.focalLength)
            cv.line(self.frame, (int(0), int(self.screenHeight / 2)), (int(self.cx(blue_area)), int(self.cy(blue_area))), (0, 255, 0), 2)
            # cv.putText(self.frame, "Area detected...", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv.LINE_4)

    def snapshot(self):
        i = 0
        while (i < 5):
            #delete the image if exists prior to generating a new one
            if os.path.exists("assets/capture"+str(i)+".png"):
                os.remove("assets/capture"+str(i)+".png")

            cv.imwrite("assets/capture"+str(i)+".png", self.frame)
            i += 1

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

    # Get the width of the object in pixels
    # def getPixelWidth(self, img):
    #     # define range of blue color in HSV
    #     lower_blue = np.array([110, 50, 50])
    #     upper_blue = np.array([130, 255, 255])

    #     # Threshold the HSV image to get only blue colors
    #     mask = cv.inRange(img, lower_blue, upper_blue)

    #     bluecnts = self.findContours(mask.copy())
    #     if (len(bluecnts) > 0):
    #         blue_area = max(bluecnts, key=cv.contourArea)



    #     return cv.minAreaRect(blue_area)

    # Calculate the focal length of the camera
    def getFocalLength(self, pixelWidth, distance, width):
        self.focalLength = (pixelWidth * distance) / width
        print("focalLength: " + str(self.focalLength))

    # Calculate the distance to an object
    def getDistance(self, pixelWidth, width=WIDTH_OBJECT):
        if self.focalLength:
            return (width * self.focalLength) / pixelWidth
        else:
            raise ValueError("Focal length was not calculated")

    def widthToCm(self, p, d, f):
        w = (p * d) / f
        print("Width in cm: " + str(w))
        return w
