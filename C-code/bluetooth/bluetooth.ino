//Library
#include "BluetoothSerial.h"
#include <ArduinoJson.h>
#include "esp_bt_device.h"
#include <Adafruit_SSD1327.h>
#include <Adafruit_GFX.h>

const int Battery_voltage = 25;

//LEDs
const int LED_Drive = 4;
const int LED_Gripper = 17;
const int LED_RJ = 5;
const int LED_RJ2 = 18;

//Push Buttons
const int KnopPush1 = 2;
const int KnopPush2 = 15;

int KnopPush1_state = 0;
int KnopPush1_state_old = 0;
int KnopPush2_state = 0;
int KnopPush2_state_old = 0;

//Right
const int Rjoystickx = 35;
const int Rjoysticky = 32;

const int Rpush = 34;
int Rpush_state = 0; 

int Rjoyvaluex = 0;
int Rjoyvaluey = 0;

int Rstate = 0;
int Rknop_oud = 0;

String RXstr ="RX";
char RXchar [7];

String RYstr ="RY";
char RYchar [7];
//-------------------------------------
//left
const int Ljoystickx = 14;
const int Ljoysticky = 33;

const int Lpush = 12;
int Lpush_state =0; 

int Ljoyvaluex = 0;
int Ljoyvaluey = 0;

int Lstate = 0;
int Lknop_oud = 0;

String LXstr ="LX";
char LXchar [7];

String LYstr ="LY";
char LYchar [7];

// IN USE: CASTS CHARARRAY BACK TO STRING -> CAN BE REMOVED ONCE THIS VERSION IS DEFINITIVE
String aStringObject;
//------------------------------------

// Check if Bluetooth configs are enabled
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Used for I2C or SPI
#define OLED_RESET -1

// I2C
Adafruit_SSD1327 display(128, 128, &Wire, OLED_RESET, 1000000);

// Bluetooth Serial object
BluetoothSerial SerialBT;

//Receive messages
char incomingChar;
String message = "";

//Timer
unsigned long previousMillis = 0;
const long interval = 100;

void setup() {
  Serial.begin(115200);
  // Bluetooth device name
  SerialBT.begin("ESP32groep6");

  if ( ! display.begin(0x3C) ) {
     Serial.println("Unable to initialize OLED");
     while (1) yield();
  }
   pinMode(Rpush, INPUT);
   pinMode(Lpush, INPUT);
   pinMode(KnopPush1, INPUT);
   pinMode(KnopPush2, INPUT);
   pinMode(LED_Drive, OUTPUT);
   pinMode(LED_Gripper, OUTPUT);
   pinMode(LED_RJ, OUTPUT);
   pinMode(LED_RJ2, OUTPUT);
   pinMode(Battery_voltage, INPUT);
}

void loop() {
  aStringObject = LYstr, LXstr, RYstr, RXstr; 
  
  DynamicJsonBuffer jBuffer;
  JsonObject& root = jBuffer.createObject();
  
  unsigned long currentMillis = millis();
  
    //push buttons
    Rpush_state = digitalRead(Rpush);
    Lpush_state = digitalRead(Lpush);
    KnopPush1_state = digitalRead(KnopPush1);
    KnopPush2_state = digitalRead(KnopPush2);
    
    //Druk knop 1
    /*if (KnopPush1_state_old != KnopPush1_state) {
        KnopPush1_state_old = KnopPush1_state;
        if(KnopPush1_state == HIGH){
           switch(KnopPush1_state) {
             case 0:
                KnopPush1_state = 1;
                break; 
           
             case 1:
                KnopPush1_state = 0;
                break; 
          }
        }      
     }*/ 

    if (KnopPush2_state_old != KnopPush2_state) {
        KnopPush2_state_old = KnopPush2_state;
        if(KnopPush2_state == HIGH){
          Lstate = 0;
          Rstate = 0;
        }      
     }  
    //Druk knop 2
    /*if (KnopPush2_state_old != KnopPush2_state) {
        KnopPush2_state_old = KnopPush2_state;
        if(KnopPush2_state == HIGH){
          Lstate = 0;
          Rstate = 0;
           switch(KnopPush2_state) {
             case 0:
                KnopPush2_state = 1;
                break; 
           
             case 1:
                KnopPush2_state = 0;
                break; 
          }
        }      
     }*/  

    //Left joystick button
    if(Lpush_state != Lknop_oud){
      Lknop_oud = Lpush_state;
      
      if(Lpush_state == HIGH){
        Rstate = 0;
         switch(Lstate) {
           case 0:
              Lstate = 1;
              break; /* optional */
         
           case 1:
              Lstate = 2;
              break; /* optional */
          
           /* you can have any number of case statements */
           case 2: /* Optional */
           Lstate = 1;
           break;
        }
      }     
    }

    if(Lstate == 0){
      digitalWrite(LED_Drive, LOW);
      digitalWrite(LED_Gripper, LOW);      
    }    
    if(Lstate == 1){
      digitalWrite(LED_Drive, HIGH);
      digitalWrite(LED_Gripper, LOW);      
    }
    if(Lstate == 2){
      digitalWrite(LED_Drive, LOW);
      digitalWrite(LED_Gripper, HIGH);        
    }

    //Right joystick button
    if(Rpush_state != Rknop_oud){
      Rknop_oud = Rpush_state;
      
      if(Rpush_state == HIGH){
        Lstate = 0;
         switch(Rstate) {
           case 0:
              Rstate = 1;
              break; /* optional */
         
           case 1:
              Rstate = 2;
              break; /* optional */
          
           /* you can have any number of case statements */
           case 2: /* Optional */
           Rstate = 3;
           break;

           case 3:
              Rstate = 1;
              break; /* optional */
        }
      }     
    }
    //LED status
    if(Rstate == 0 and Lstate == 0){
      digitalWrite(LED_RJ, LOW);
      digitalWrite(LED_RJ2, LOW);
      digitalWrite(LED_Drive, LOW);
      digitalWrite(LED_Gripper, LOW);              
    }
    if(Rstate == 1){
      digitalWrite(LED_RJ, HIGH);
      digitalWrite(LED_RJ2, LOW);      
    }
    if(Rstate == 2){
      digitalWrite(LED_RJ, LOW);
      digitalWrite(LED_RJ2, HIGH);        
    }
    if(Rstate == 3){
      digitalWrite(LED_RJ, LOW);
      digitalWrite(LED_RJ2, LOW);        
    }    
  //waardes op scherm laten zien en versturen via Bluetooth
  if (currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;
 
    //display schoonmaken
    display.clearDisplay();
    testdrawrect();
    
    //Y waarde Left
    Ljoyvaluey = analogRead(Ljoysticky);
    display.setCursor(3,20);
    display.print("LY = ");
    if(Lstate ==2){
      if(Ljoyvaluey > 4000){
        display.print("Lift up");
      }
      else if(Ljoyvaluey <1){
        display.print("Lift down");
      }
      else {
        display.print("Lift standby");
      }
    }
    if(Lstate == 1){
      if(Ljoyvaluey > 4000){
        display.print("F Forward");
      }
      else if(Ljoyvaluey <1){
        display.print("F Backwards");
      }
      else if(Ljoyvaluey > 0 and Ljoyvaluey <1910){
        display.print("S Backwards");
      }
      else if(Ljoyvaluey > 1935 and Ljoyvaluey <4001){
        display.print("S Fowards");
      }  
      else {
        display.print("Hold");
      }      
    }
    if(Lstate == 0){
      display.print("standby");
    }
    
    //X waarde Left
    Ljoyvaluex = analogRead(Ljoystickx);
    display.setCursor(3,30);
    display.print("LX = Not Used");    
      
    //Y waarde Right
    Rjoyvaluey = analogRead(Rjoysticky);
    display.setCursor(3,40);
    display.print("RY = ");
    if(Lstate == 1){
      if(Rjoyvaluey > 4000){
        display.print("F Forward");
      }
      else if(Rjoyvaluey <1){
        display.print("F Backwards");
      }
      else if(Rjoyvaluey > 0 and Rjoyvaluey <1917){
        display.print("S Backwards");
      }
      else if(Rjoyvaluey > 1990 and Rjoyvaluey <4001){
        display.print("S Fowards");
      }  
      else {
        display.print("Hold");
      }      
    }
    if(Lstate == 0){
      display.print("standby");
    }
    if(Lstate == 2){
      display.print("Not Used");
    }
    
    //X waarde Right
    Rjoyvaluex = analogRead(Rjoystickx);
    display.setCursor(3,50);
    display.print("RX = ");
    if(Lstate == 2){
      if(Rjoyvaluex > 4000){
        display.print("Gripper close");
      }
      else if(Rjoyvaluex <1){
        display.print("Gripper open ");
      }
      else {
        display.print("Gripper standby");
      }
    }
    if(Lstate == 0){
      display.print("standby");
    }
    if(Lstate == 1){
      display.print("Not Used");
    }
    
    LYstr = String(Ljoyvaluey);
    LXstr = String(Ljoyvaluex);
    RYstr = String(Rjoyvaluey);
    RXstr = String(Rjoyvaluex);
    
    root["LY"] = String(Ljoyvaluey);
    root["LX"] = String(Ljoyvaluex);
    root["RY"] = String(Rjoyvaluey);
    root["RX"] = String(Rjoyvaluex);
    root["driveOrGrip"] = String(Lstate);
    root["flag"] = String(Rstate);
//    root["dance"] = String(KnopPush2_state);
    

    String json;
    root.printTo(json);
    Serial.println(json);//THIS LINE SHOULD BE REMOVED ONCE WE INTEGRATE
    SerialBT.println(json);
    
    //Controller
    display.setCursor(40,10);
    display.print("Controller");
    display.setCursor(3,70);
    display.print("Modus: ");

    //Modus weergeven
    if (Lstate == 0 and Rstate ==0 ){
      display.print("Standby");
    }
    else if (Lstate == 1){
       display.print("Drive");
    }
    else if (Lstate == 2){
      display.print("Gripper");
    }
    else if (Lstate == 0 and Rstate == 1){
      display.print("Vision");
    }
    else if (Lstate == 0 and Rstate == 2){
      display.print("Cookies");
    }
    else if (Lstate == 0 and Rstate == 3){
      display.print("Dancing");
    }

    //Robot
    display.setCursor(55,85);
    display.print("Robot");
    display.setCursor(3,95);
    display.print("Battery = ");
    display.print(" mV");
    display.setCursor(3,105); 
    display.print("Gewicht = ");
    display.print("g");
    
    //Battery voltage controller
    display.setCursor(3,60);
    display.print("Battery = ");
    display.print((float)analogRead(Battery_voltage)*0.001681727234, 2);
    display.print(" V"); 
  }

    //Op het scherm laten zien
    display.display();
    
  //Receive messages
  if (SerialBT.available()){
    char incomingChar = SerialBT.read();
    if (incomingChar != '\n'){
      message += String(incomingChar);
    }
    else{
      message = "";
    }
    //Serial.write(incomingChar);  
  }
}

void testdrawrect(void) {
  
    display.drawRect(0, 0, 128, 80, SSD1327_WHITE); 
    display.drawRect(0, 82, 128, 46, SSD1327_WHITE); 

}
