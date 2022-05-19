from controller import Robot
from math import pi


class Arm:
    motors = {}
    sensors = {}
    speed = 2
    armRadian = 0

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

    # Rotates the robot arm
    def rotateArm(self, footMotor, degrees=float('inf')):
        footMotor = self.motors.get(footMotor)

        self.armRadian += self.degreesToRadians(degrees)
        print(self.armRadian)
        footMotor.setPosition(self.armRadian)
        footMotor.setVelocity(self.speed)

    @staticmethod
    def degreesToRadians(degrees):
        return degrees / 180 * pi
