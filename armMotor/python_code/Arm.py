class Arm:
    robot = None
    timeStep = 64
    leftMotor = None
    rightMotor = None
    grabberMotor = None

    # def __init__(self, robot, timeStep, leftMotor, rightMotor, grabberMotor):
    def __init__(self, leftMotor):
        '''
            Initialize the arm and sets the arm components
                Parameters:
                    robot(Robot): sets the robot
                    timeStep(int): sets the time step where the arm works on
                    leftMotor(Motor): sets the left motor
                    rightMotor(Motor): sets the right motor
                    rightMotor(Motor): sets the grabber motor
        '''
        # self.robot = robot
        # self.timeStep = timeStep
        self.leftMotor = leftMotor
        # self.rightMotor = rightMotor
        # self.grabberMotor = grabberMotor
