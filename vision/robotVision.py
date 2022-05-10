import math
from cv2 import findContours
import numpy as np
import cv2 as cv
from threading import *


class robotVision(Thread):
    focalLength = 0

    def run(self):
        self.cap = cv.VideoCapture(1)
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

            self.hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

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
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(self.hsv, lower_blue, upper_blue)

        bluecnts = self.findContours(mask)
        if (len(bluecnts) > 0):
            #return the biggest contourArea and determine centroid
            blue_area = max(bluecnts, key=cv.contourArea)
            self.centroid(blue_area)

            (xg, yg, wg, hg) = cv.boundingRect(blue_area)
            cv.rectangle(self.frame,(xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)
            cv.putText(self.frame, "Area detected...", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv.LINE_4)

    def snapshot(self):
        i = 0
        while (i < 5):
            cv.imwrite("assets/capture"+str(i)+".png", self.frame)
            i  += 1

    def centroid(self, momentsToCalculate, draw = True):
        m = cv.moments(momentsToCalculate)
        if ((m['m10'] and m['m00']) and (m['m01'] and m['m00'])):
            #calculate centroid of mass and draw it
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            if (draw):
                cv.circle(self.frame, (cx, cy), 5, (255, 255, 255), -1)
        # return for external use
        return m

    def releaseStream(self):
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

    def imshow(self):
        cv.imshow("Video capture (Final result)", self.frame)

    def findContours(self, mask):
       return cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]


    def drawContours(self, target="default"):
        if (target == "default"):
            cv.drawContours(self.frame, self.contours, -1, (0, 255, 0), 3)
        elif (isinstance(target, list)):
            cv.drawContours(self.frame, target, -1, (0, 255, 0), 3)
        else:
            cv.drawContours(self.frame, [target], -1, (0, 255, 0), 3)

    # Calculate the focal length of the camera
    def getFocalLength(self, pixelWidth, width, distance=10):
        self.focalLength = (pixelWidth * distance) / width

    # Calculate the distance to an object
    def getDistance(self, pixelWidth, width):
        if self.focalLength:
            return (width * self.focalLength) / pixelWidth
        else:
            raise ValueError("Focal length was not calculated")
