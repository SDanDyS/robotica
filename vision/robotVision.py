import math
from cv2 import findContours
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
    # The width of the object
    WIDTH_OBJECT = 7.5
    # The distance to the object in the KNOWN_IMAGE
    KNOWN_DISTANCE = 40
    # The image that is known to be KNOWN_DISTANCE away
    KNOWN_IMAGE = 'assets/images/40cm.jpg'

    focalLength = 0

    def run(self):
        self.camIsPi = False
        
        # Check whether cam arg is Pi camera
        if self.camSelector == "pi":
            print("Selecting PiCamera")
            self.camIsPi = True
            
            resW = 320
            resH = 320
            resolution = (resW, resH)
            self.screenWidth  = resW
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
            self.screenWidth  = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
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
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([128, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(self.hsv, lower_blue, upper_blue)

        bluecnts = self.findContours(mask)
        if (len(bluecnts) > 0):
            # return the biggest contourArea and determine centroid
            blue_area = max(bluecnts, key=cv.contourArea)
            self.centroid(blue_area)
            # distance = self.getDistance(self.cx(blue_area), self.screenWidth)
            # print (distance)
            (xg, yg, wg, hg) = cv.boundingRect(blue_area)
            cv.rectangle(self.frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

            if (distance != 0):
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
    def getPixelWidth(self, img):
    #     # define range of blue color in HSV
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([128, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(img, lower_blue, upper_blue)

        bluecnts = self.findContours(mask)
        if (len(bluecnts) > 0):
            blue_area = max(bluecnts, key=cv.contourArea)

        return cv.minAreaRect(blue_area)

    # Calculate the focal length of the camera
    def getFocalLength(self, pixelWidth, distance, width):
        self.focalLength = (pixelWidth * distance) / width
        #print("focalLength: " + str(self.focalLength))

    # Calculate the distance to an object
    def getDistance(self, pixelWidth, width, focal=False):
        if (pixelWidth == 0):
            return 0
        if self.focalLength:
            return (width * self.focalLength) / pixelWidth
        elif (focal):
            ##later stages swap this to the if statement rather then elif. Right now it is never reached
            return (width * focal) / pixelWidth
        else:
            raise ValueError("Focal length was not calculated")

    def widthToCm(self, pixel, distance, focal):
        w = (pixel * distance) / focal
        print("CM: " + str(w))
        return w
