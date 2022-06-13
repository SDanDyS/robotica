from math import pi
import numpy as np
import Servo


class Motor:
    robot = None
    timeStep = 64
    motor = None
    maxSpeed = 1.5
    motorMin = None
    motorMax = None
    motorRadian = 0

    # id = 1

    # def __init__(self, robot, timeStep, motorName, sensorName):
    def __init__(self):
        '''
            Initialize the motor
                Parameters:
                    robot(Robot): sets the robot
                    timeStep(int): sets the time step where the motor works on
                    motorName(string): the name to get the motor device
                    sensorName(string): the name to get the sensor device
        '''
        # self.robot = robot
        # self.timeStep = timeStep
        self.servo = Servo(0xb, 0x41)
        self.servo.servo_installation_position()

        # Add the motor
        # self.motor = self.robot.getDevice(motorName)
        # self.motor.setPosition(0.0)
        # self.motor.setVelocity(0.0)

        # Add the sensor
        # self.sensor = self.robot.getDevice(sensorName)
        # self.sensor.enable(self.timeStep)

    # def __init__(self, id):
    #     self.id = id

    def getName(self):
        '''Returns the name of the motor'''
        return self.motor.getName()

    def setMotorBoundaries(self, minDegree, maxDegree):
        '''
        Sets the boundaries of how much the motor can move.
            Parameters:
                minDegree(float): The minimum degree the motor can move
                maxDegree(float): the maximum degree the motor can move
        '''
        self.motorMin = np.round(self.degreesToRadians(minDegree), 10)
        self.motorMax = np.round(self.degreesToRadians(maxDegree), 10)

    def rotateDegrees(self, degrees=float('inf'), speed=0):
        '''
        Rotates the motor.
            Parameters:
                degrees(float): the amount de motor needs to rotate
                speed(int): the speed the motor moves at
        '''
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

    @ staticmethod
    def degreesToRadians(degrees):
        '''Converts from degrees to radian'''
        return degrees / 180 * pi
