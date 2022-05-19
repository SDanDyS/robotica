from controller import Robot


class Arm:
    motors = {}
    sensors = {}

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
