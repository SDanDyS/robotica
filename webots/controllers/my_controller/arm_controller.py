class Arm:
    robot = None
    timeStep = 64
    rotationMotor = None
    firstRodMotor = None

    def __init__(self, robot, timeStep, rotationMotor, firstRodMotor):
        self.robot = robot
        self.timeStep = timeStep
        self.rotationMotor = rotationMotor
        self.firstRodMotor = firstRodMotor
