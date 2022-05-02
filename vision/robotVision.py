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
            print("test robot multithreader")
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
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.blur = cv.GaussianBlur(gray,(5, 5), 0)
        _, self.thresh = cv.threshold(self.blur, 75, 255, 0, cv.THRESH_BINARY)
        self.thresh = cv.erode(self.thresh, None, iterations = 3)
        self.findContours()

        for contour in self.contours:
            (x, y, w, h) = cv.boundingRect(contour)

            # if (cv.contourArea(contour) < 20):
            #     continue
            
            # cv.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.generateConvexHull()
        self.drawContours(self.convex_hull)

    def releaseStream(self):
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

    def imshow(self):
        cv.imshow("videoFrame", self.frame)

    def findContours(self):
        self.contours, self.hierarchy = cv.findContours(self.thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    def generateConvexHull(self):
        self.convex_hull = []
        for cnt in self.contours:
            hull = cv.convexHull(cnt)
            self.convex_hull.append(hull)

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

class test(Thread):
    def run(self):
        while True:
            print("sync call")