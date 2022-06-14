#include <AX12A.h>
#include <Wire.h>

#define DirectionPin   (2u)
#define BaudRate      (1000000ul)
//#define ID4       (254u) 
#define ID1       (16u)
#define ID2       (13u)
#define ID3       (7u)


int reg = 0;
int reg1 = 0;
int pos = 0;
int pos1 = 0;

void setup()
{
   // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  Serial.begin(BaudRate);
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  delay(1000);
  ax12a.begin(BaudRate, DirectionPin, &Serial);

int position1 = 0;
int position2 = 0;
}

void stopServo(int servoId) {
  ax12a.setEndless(servoId, OFF);
//  int posision = ax12a.readPosition(servoId);
 // ax12a.setMaxTorque(servoId, 0);
  ax12a.setVoltageLimit(servoId, 0, 0);
//  ax12a.moveSpeed(servoId, posision, 400);
}

void startServo(int servoId) {
  ax12a.setMaxTorque(servoId, 1023);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    if(c == 1){
       ax12a.turn(ID1,LEFT,200);
        ax12a.turn(ID2,RIGHT,200); 
          }
       if(c == 2){

       ax12a.turn(ID1,RIGHT,200);   
       ax12a.turn(ID2,LEFT,200); 
       }
       if(c == 3){
       ax12a.turn(ID3,RIGHT,300);   
       }

    if(c == 4){
       ax12a.turn(ID3,LEFT,400);                  
       }
     if(c == 5){
        ax12a.turn(ID3,LEFT,0);
        
     }

     if(c == 0){       
        ax12a.turn(ID1,LEFT,0);
        ax12a.turn(ID2,LEFT,0);
        
     }
delay(1000);       
  }
}
void loop()
{

}
