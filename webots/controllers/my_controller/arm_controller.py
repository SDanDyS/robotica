from controller import Robot
from math import pi
import numpy as np


class Arm:
    motors = {}
    sensors = {}
    rotationSpeed = firstRodSpeed = 1.5
    armRadian = firstRodRadian = 0

    def __init__(self, robot):
        self.robot = robot

    # Adds all the motors of the arm
    def addMotors(self, motors):
        for motor in motors:
            robotMotor = self.robot.getDevice(motor)
            robotMotor.setVelocity(0.0)
            self.motors[motor] = robotMotor

    # Adds all the sensors of the arm
    def addSensors(self, sensors, timestamp):
        for sensor in sensors:
            robotSensor = self.robot.getDevice(sensor)
            robotSensor.enable(timestamp)

    def setFirstRodBoundaries(self, minDegree, maxDegree):
        self.firstRodMin = np.round(self.degreesToRadians(minDegree), 10)
        self.firstRodMax = np.round(self.degreesToRadians(maxDegree), 10)

    # Rotates the robot arm
    def rotateArm(self, footMotor, degrees=float('inf')):
        footMotor = self.motors.get(footMotor)

        self.armRadian += np.round(self.degreesToRadians(degrees), 10)
        self.armRadian = np.round(self.armRadian, 10)
        footMotor.setPosition(self.armRadian)
        footMotor.setVelocity(self.rotationSpeed)

    # Move the first rod of the robot arm
    def moveFirstRod(self, firstRod, degrees=float('inf')):
        firstRodMotor = self.motors.get(firstRod)

        if (hasattr(self, "firstRodMin") and hasattr(self, "firstRodMax")):
            radians = self.firstRodRadian + \
                np.round(self.degreesToRadians(degrees), 10)

            if (radians >= self.firstRodMin and radians <= self.firstRodMax):
                self.firstRodRadian = radians
        else:
            self.firstRodRadian += np.round(self.degreesToRadians(degrees), 10)
            self.firstRodRadian = np.round(self.firstRodRadian, 10)

        print(self.firstRodRadian)

        firstRodMotor.setPosition(self.firstRodRadian)
        firstRodMotor.setVelocity(self.firstRodSpeed)

    @ staticmethod
    def degreesToRadians(degrees):
        return degrees / 180 * pi
