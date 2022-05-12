from controller import Robot, Motor, Keyboard

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


while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()
    if key in motor_cmd.keys():
        command_motors((motor_cmd[key]))
pass
