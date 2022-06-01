from math import pi
import numpy as np


class Motor:
    robot = None
    timeStep = 64
    motor = None
    maxSpeed = 1.5
    motorMin = None
    motorMax = None
    motorRadian = 0

    def __init__(self, robot, timeStep, motorName, sensorName):
        self.robot = robot
        self.timeStep = timeStep

        # Add the motor
        self.motor = self.robot.getDevice(motorName)
        self.motor.setPosition(0.0)
        self.motor.setVelocity(0.0)

        # Add the sensor
        self.sensor = self.robot.getDevice(sensorName)
        self.sensor.enable(self.timeStep)

    # Get the name of the motor
    def getName(self):
        return self.motor.getName()

    # Set the boundaries of how much the first rod can move
    def setMotorBoundaries(self, minDegree, maxDegree):
        self.motorMin = np.round(self.degreesToRadians(minDegree), 10)
        self.motorMax = np.round(self.degreesToRadians(maxDegree), 10)

    # Rotate the rod
    def rotateDegrees(self, degrees=float('inf'), speed=0):
        # Check if boundary is set
        if self.motorMin != None and self.motorMax != None:
            radians = self.motorRadian + \
                np.round(self.degreesToRadians(degrees), 10)

            if (radians >= self.motorMin and radians <= self.motorMax):
                self.motorRadian = radians
        else:
            self.motorRadian += np.round(self.degreesToRadians(degrees), 10)
            self.motorRadian = np.round(self.motorRadian, 10)

        speed = self.maxSpeed if not speed else speed
        self.motor.setVelocity(speed)
        self.motor.setPosition(self.motorRadian)

    # Convert from degrees to radian
    @ staticmethod
    def degreesToRadians(degrees):
        return degrees / 180 * pi
