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

void setup()
{
//  Dynamixel.setSerial(&Serial1)
  ax12a.begin(BaudRate, DirectionPin, &Serial);
//  Serial.begin(9600);
//  SetPosition(leftMotor, 0) // position: 0 - 1023, 512 = middel
}

void loop()
{
  turnMotor(leftMotor, 1, 300)
  
}
