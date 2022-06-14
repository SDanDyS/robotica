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
//  ax12a.setEndless(ID1, ON);
// ax12a.turn(ID1,RIGHT,100);
//ax12a.reset(ID4);
//ax12a.setID(ID,ID2);
//ax12a.setEndless(ID2, ON);
// ax12a.turn(ID2,LEFT,200);
//  reg = ax12a.readTemperature(ID1);
 // reg1 = ax12a.readTemperature(ID2);
// pos = ax12a.readPosition(ID1);
// pos1 = ax12a.readPosition(ID2);  
int position1 = 0;
int position2 = 0;
//int setAngleLimit(ID3, 0, 512);
  
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
//  ax12a.setVoltageLimit(servoId, 160, 160);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    if(c == 1){
      
       //ax12a.setEndless(ID1, ON);
       ax12a.turn(ID1,LEFT,200); 
      
       
       // ax12a.moveSpeed(ID1,500,100);
        //delay(1000);
   
        //ax12a.setEndless(ID2, ON);
        ax12a.turn(ID2,RIGHT,200); 
       
       
       //ax12a.moveSpeed(ID2,500,100);
      //   delay(1000);
     
    
   //       ax12a.setEndless(ID3, OFF);
  //     ax12a.turn(ID2,LEFT,200); 
  //        ax12a.moveSpeed(ID3,200,100);
  //        delay(1000);
          }
       if(c == 2){
        
       //ax12a.setEndless(ID1, ON);
       //ax12a.moveSpeed(ID1,200,50);
       ax12a.turn(ID1,RIGHT,200);   
        //ax12a.moveSpeed(ID1,200,100);
       // delay(1000);
   
      // ax12a.setEndless(ID2, ON);
       //ax12a.moveSpeed(ID2,200,50);
       ax12a.turn(ID2,LEFT,200); 
       //ax12a.moveSpeed(ID1,200,100);
       
       }
       if(c == 3){
      
      
        ax12a.setEndless(ID3, ON);
       ax12a.turn(ID3,RIGHT,300);   
       // ax12a.moveSpeed(ID1,200,100);
        
   
        
       
       }

    if(c == 4){
      
      
        //ax12a.setEndless(ID3, ON);
       ax12a.turn(ID3,LEFT,400);   
       // ax12a.moveSpeed(ID1,200,100);
       // delay(1000);
   
        
       
       }
     if(c == 5){
        ax12a.turn(ID3,LEFT,0);
        
     }

     if(c == 0){
      //1 servo draait links andere draait rechtsom 
       // ax12a.setEndless(ID2, OFF);
       // ax12a.turn(ID2,LEFT,200); 
//        ax12a.setEndless(ID1, OFF);
//          ax12a.setEndless(ID2, OFF);
//        int posision = ax12a.readPosition(ID1);
//        int posision2 = ax12a.readPosition(ID2);
//        Serial.println(posision);
//        Serial.println(posision2);
//        ax12a.moveSpeed(ID1, posision, 200);
//        ax12a.moveSpeed(ID2, posision2, 200);
        
        ax12a.turn(ID1,LEFT,0);
        ax12a.turn(ID2,LEFT,0);
        //stopServo(ID1);
        //stopServo(ID2);
        
        
      
  //     ax12a.turn(ID2,LEFT,200); 
       // ax12a.moveSpeed(ID2,200,100);
        
     }
delay(1000);
    
    
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
