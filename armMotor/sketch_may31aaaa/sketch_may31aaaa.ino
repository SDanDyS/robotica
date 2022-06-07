#include <AX12A.h>
#include <Wire.h>

#define DirectionPin   (2u)
#define BaudRate      (1000000ul)
//#define ID4       (254u) 
#define ID1       (11u)
#define ID2       (13u)
#define ID3       (16u)


int reg = 0;
int reg1 = 0;
int pos = 0;
int pos1 = 0;

void setup()
{
   // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  delay(1000);
  ax12a.begin(BaudRate, DirectionPin, &Serial);
//  ax12a.setEndless(ID1, ON);
// ax12a.turn(ID1,RIGHT,100);
//ax12a.reset(ID4);
//ax12a.setID(ID,ID2);
//ax12a.setEndless(ID2, ON);
// ax12a.turn(ID2,LEFT,200);
//  reg = ax12a.readTemperature(ID1);
 // reg1 = ax12a.readTemperature(ID2);
//  pos = ax12a.readPosition(ID1);
//  pos1 = ax12a.readPosition(ID2);  
  
}
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    if(c == 1){
     ax12a.setEndless(ID1, OFF);
  //     ax12a.turn(ID2,LEFT,200); 
       ax12a.moveSpeed(ID1,200,100);
       delay(1000);
            ax12a.setEndless(ID2, OFF);
  //     ax12a.turn(ID2,LEFT,200); 
       ax12a.moveSpeed(ID2,200,100);
       delay(1000);
            ax12a.setEndless(ID3, OFF);
  //     ax12a.turn(ID2,LEFT,200); 
       ax12a.moveSpeed(ID3,200,100);

delay(1000);
    }
    else{
//      ax12a.setEndless(ID2, OFF);
  }
    
  }
}
void loop()
{
/*  pos = ax12a.readPosition(ID1);
  pos1 = ax12a.readPosition(ID2); 
 Serial.print(" 1: ");
 Serial.print(reg);
 Serial.print(pos);
 Serial.print("\t");
 Serial.print("2: ");
 Serial.println(reg1);
 Serial.println(pos1);
 
 delay(1000);*/
}
