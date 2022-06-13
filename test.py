import math
from cv2 import findContours
from distance.HCSRO4Component import *
from drive.dcMotorIndu import *
import numpy as np
import cv2 as cv
from threading import *
import os
import time
import logging

i = 0
j = 0
fooStop = False
testStop = False

class Test(Thread):
    def run(self):
        while True:
            print("Request class test")
            global testStop
            global fooStop
            if (testStop == True):
                fooStop = True
                break

class Foo(Thread):
    def run(self):
        while True:
            print("Request class Foo")
            global fooStop
            if (fooStop == True):
                break

while (j < 5):
    if (i == 0):
        t = Test()
        t.start()
        i += 1
    else:
        testStop = True
        f = Foo()
        f.start()
    j += 1
