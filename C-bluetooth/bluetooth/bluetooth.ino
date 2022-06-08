//Library
#include "BluetoothSerial.h"
#include <ArduinoJson.h>
#include "esp_bt_device.h"
#include <Adafruit_SSD1327.h>
#include <Adafruit_GFX.h>

DynamicJsonBuffer jBuffer;
JsonObject& root = jBuffer.createObject();

const int Battery_voltage = 25;
const int LED_Drive = 16;
const int LED_Gripper = 17;

//Push Buttons
const int KnopPush1 = 4;
const int KnopPush2 = 15;

int KnopPush1_state = 0;
int KnopPush2_state = 0;

//Right
const int Rjoystickx = 34;
const int Rjoysticky = 35;

const int Rpush = 14;
int Rpush_state =0; 

int Rjoyvaluex = 0;
int Rjoyvaluey = 0;

String RXstr ="RX";
char RXchar [7];

String RYstr ="RY";
char RYchar [7];
//-------------------------------------
//left
const int Ljoystickx = 32;
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
}

void loop() {
 
  unsigned long currentMillis = millis();
  
  //push buttons
    Rpush_state = digitalRead(Rpush);
    Lpush_state = digitalRead(Lpush);
    KnopPush1_state = digitalRead(KnopPush1);
    KnopPush2_state = digitalRead(KnopPush2);
    
    if(KnopPush1_state == HIGH){
      Serial.println("knop1");
    }
    if(KnopPush2_state == HIGH){
      Serial.println("knop2");
    }

    if(Lpush_state != Lknop_oud){
      Lknop_oud = Lpush_state;
      
      if(Lpush_state == HIGH){
        if(Lstate == 0){
          Lstate = 1;
        }
        else if(Lstate == 1){
          Lstate = 2;
        }
        else if(Lstate == 2){
          Lstate = 1;
        }
      }     
    }

    if(Lstate == 1){
      digitalWrite(LED_Drive, HIGH);
      digitalWrite(LED_Gripper, LOW);      
    }
    if(Lstate == 2){
      digitalWrite(LED_Drive, LOW);
      digitalWrite(LED_Gripper, HIGH);        
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
    display.print("Y waarde L = ");
    display.print(Ljoyvaluey);
  
    //X waarde Left
    Ljoyvaluex = analogRead(Ljoystickx);
    display.setCursor(3,30);
    display.print("x waarde L = ");
    display.print(Ljoyvaluex);
      
    
    //Y waarde Right
    Rjoyvaluey = analogRead(Rjoysticky);
    display.setCursor(3,40);
    display.print("Y waarde R = ");
    display.print(Rjoyvaluey);
    
    //X waarde Right
    Rjoyvaluex = analogRead(Rjoystickx);
    display.setCursor(3,50);
    display.print("x waarde R = ");
    display.print(Rjoyvaluex);
    
    LYstr = String(Ljoyvaluey);
    LXstr = String(Ljoyvaluex);
    RYstr = String(Rjoyvaluey);
    RXstr = String(Rjoyvaluex);
    
    root["LY"] = String(Ljoyvaluey);
    root["LX"] = String(Ljoyvaluex);
    root["RY"] = String(Rjoyvaluey);
    root["RX"] = String(Rjoyvaluex);

    String json;
    root.printTo(json);
    Serial.println(json);//THIS LINE SHOULD BE REMOVED ONCE WE INTEGRATE
    SerialBT.println(json);
    
    //Robot
    display.setCursor(55,10);
    display.print("Robot");
    
    //Battery voltage
    display.setCursor(3,60);
    display.print("Battery = ");
    display.print((float)analogRead(Battery_voltage)*0.001721727234, 2);
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

}
