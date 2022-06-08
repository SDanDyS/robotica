from controller import Robot, Keyboard
from arm_controller import Arm
from Motor import Motor

TIME_STEP = 64

MAX_SPEED = 2
CRUISING_SPEED = 0.3
TURN_SPEED = CRUISING_SPEED / 2.0

# create the Robot instance.
robot = Robot()

# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left motor')
rightMotor = robot.getDevice('right motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
rightMotor.setVelocity(0.0)
leftMotor.setVelocity(0.0)

# set up the motor speeds at 10% of the MAX_SPEED.
# leftMotor.setVelocity(0.0 * MAX_SPEED)
# rightMotor.setVelocity(0.0 * MAX_SPEED)

# Setup the robot arm
leftMotor = Motor(robot, TIME_STEP, "foot motor", "foot sensor")
rightMotor = Motor(robot, TIME_STEP, "first rod motor", "first rod sensor")
grabberMotor = Motor(robot, TIME_STEP, "first rod motor", "first rod sensor")

arm = Arm(robot, TIME_STEP, leftMotor, rightMotor, grabberMotor)
# arm.leftMotor.maxSpeed = 5

# arm.rightMotor.maxSpeed = 1.5
# arm.rightMotor.setMotorBoundaries(0, 120)

# Setup the keyboard
keyboard = Keyboard()
keyboard.enable(TIME_STEP)

motor_cmd = {
    ord('W'): (CRUISING_SPEED, CRUISING_SPEED),
    ord('S'): (-CRUISING_SPEED, -CRUISING_SPEED),
    ord('D'): (-TURN_SPEED, TURN_SPEED),
    ord('A'): (TURN_SPEED, -TURN_SPEED),
    ord('Q'): (0.0, 0.0),
    ord('P'): (MAX_SPEED, MAX_SPEED)
}


def command_motors(cmd):
    leftMotor.setVelocity(cmd[0])
    rightMotor.setVelocity(cmd[1])


def armJoystickMovement(motor, value, maxSpeed, degrees):
    if value > 1:
        value = 1
    elif value < -1:
        value = -1

    rotationSpeed = maxSpeed * value

    if value >= 0:
        motor.rotateDegrees(degrees, rotationSpeed)
    elif value < 0:
        motor.rotateDegrees(-degrees, rotationSpeed)


while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()
    if key in motor_cmd.keys():
        command_motors((motor_cmd[key]))

    # Move the arm based on the input
    if key == ord('J'):
        arm.rotationMotor.rotateDegrees(10)
    elif key == ord('L'):
        arm.rotationMotor.rotateDegrees(-10)
    elif key == ord('K'):
        arm.firstRodMotor.rotateDegrees(5)
    elif key == ord('I'):
        arm.firstRodMotor.rotateDegrees(-5)
pass

# if(afstand < 20):
#leftMotor.setVelocity(0.1 * MAX_SPEED)
#rightMotor.setVelocity(-0.1 * MAX_SPEED)
# else:
#leftMotor.setVelocity(0.1 * MAX_SPEED)
#rightMotor.setVelocity(0.1 * MAX_SPEED)
