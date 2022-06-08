#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

#include <AX12A.h>
//#include <DynamixelSerial.h>
//#include <DynamixelShield.h>
//#include <BioloidController.h>

#define DirectionPin    (2u)
#define BaudRate        (1000000ul)


// Define the servo's
//#define ID4           (254u) 
#define leftMotor       (11u)
#define rightMotor      (13u)
#define grabberMotor    (16u)

void turnMotor(unsigned int id, bool toRight, int speed)
void moveMotor(unsigned int id, int position)
int getPosition(unsigned int id)
int square(int i)

#endif
