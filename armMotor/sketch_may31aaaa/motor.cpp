#include "motor.h"

void turnMotor(unsigned int id, bool toRight, int speed)
{
  ax12a.turn(id, (toRight ? RIGHT : LEFT), speed)
}

void moveMotor(unsigned int id, int position)
{
  ax12a.move(id, position)
}

int getPosition(unsigned int id)
{
  return ax12a.readPosition(id)
}

int square(int i)
{
  return i * i;
}
