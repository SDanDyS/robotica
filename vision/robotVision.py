import math
import numpy as np
import cv2 as cv
from threading import *

class robotVision(Thread):

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

            if (self.FLAG == 1):
                self.detectCookie()
            else:
                self.detectMovingObject()

            self.imshow()

            if cv.waitKey(1) == ord('q'):
                self.releaseStream()
                break

    def detectMovingObject(self):
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(hsv, lower_blue, upper_blue)

        result = cv.bitwise_and(self.frame, self.frame, mask = mask)

        self.frame = result

    def detectCookie(self):
        # turn scene gray and put a threshold on noise
        self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.blur = cv.GaussianBlur(self.gray,(39, 39), 0)#75 75 works good too
        _, self.thresh = cv.threshold(self.blur, 75, 255, 0, cv.THRESH_BINARY)
        self.dilated = cv.dilate(self.thresh, (7, 7), iterations = 3)
        self.findContours()

        for cnt in self.contours:
            area = cv.contourArea(cnt)
            perimeter = cv.arcLength(cnt, True)

            m = cv.moments(cnt)

            if ((m['m10'] and m['m00']) and (m['m01'] and m['m00'])):
                #calculate centroid of mass
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])

            if (perimeter != 0 and area != 0):
                #the rounding -> how round it is
                formFactor = 4 * math.pi * area / perimeter**2

            if (area > 100):
                self.drawContours(cnt)
        # self.drawContours()

    def releaseStream(self):
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

    def imshow(self):
        cv.imshow("Gray capture (First cycle)", self.gray)
        cv.imshow("Blur capture (Second cycle)", self.blur)
        cv.imshow("Thresh capture (Third cycle)", self.thresh)
        cv.imshow("Dilated capture (Fourth cycle)", self.dilated)
        cv.imshow("Video capture (Final result)", self.frame)

    def findContours(self):
        self.contours, self.hierarchy = cv.findContours(self.dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    def drawContourBasedOnArea(self):
        for cnt in self.contours:
            area = cv.contourArea(cnt)
            perimeter = cv.arcLength(cnt, True)

            if (perimeter != 0 and area != 0):
                formFactor = 4 * math.pi * area / perimeter**2

            if (area > 1000):
                self.drawContours(cnt)

    def drawContours(self, target = "default"):
        if (target == "default"):
            cv.drawContours(self.frame, self.contours, -1, (0,255,0), 3)
        elif (isinstance(target, list)):
            cv.drawContours(self.frame, target, -1, (0,255,0), 3)
        else:
            cv.drawContours(self.frame, [target], -1, (0,255,0), 3)