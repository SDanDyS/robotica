from distance.HCSRO4Component import *
print(sensorDistance())


# import numpy as np
# import cv2 as cv

# def isBadContour(c):
#     # approximate the contour
#     peri = cv.arcLength(c, True)
#     approx = cv.approxPolyDP(c, 0.02 * peri, True)
#     # the contour is 'bad' if it is not a rectangle
#     return not len(approx) == 4

# cap = cv.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
    
#     hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                
#     # define range of black color in HSV
#     lower_val = np.array([0,0,0])
#     upper_val = np.array([179,100,30])
#     # Threshold the HSV image to get only black colors
#     mask = cv.inRange(hsv, lower_val, upper_val)
#     cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
#     abscnts = []
#     if (len(cnts) > 0):
#         for cnt in cnts:
#             if (isBadContour(cnt) == False):
#                 abscnts.append(cnt)
#         area = max(cnts, key=cv.contourArea)
#         (xg, yg, wg, hg) = cv.boundingRect(area)
#         cv.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)
   
   
   
#     res = cv.bitwise_and(frame, frame, mask= mask)

#     # invert the mask to get black letters on white background

#     res2 = cv.bitwise_not(mask)

#     # display image

#     cv.imshow("img", res)
#     cv.imshow("img2", res2)
#     cv.imshow("hsv mode", frame)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()