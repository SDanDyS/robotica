#include <HX711_ADC.h>
#include <Wire.h>
#include <AX12A.h>

#define SLAVE_ADDRESS 0x8
#define DirectionPin   (2u)
#define BaudRate      (1000000ul)
//#define ID4       (254u) 
#define ID1       (4u)
#define ID2       (13u)
#define ID3       (7u)

#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

//pins:
const int HX711_dout = 8; //mcu > HX711 dout pin
const int HX711_sck = 7; //mcu > HX711 sck pin

int reg = 0;
int reg1 = 0;
int pos = 0;
int pos1 = 0;

bool start_new_cycle = false;
bool only_voltage = true;
char buf[10] = {};
int index = 0;

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

const int battery_voltage = 17;

void setup() {
  Serial.begin(BaudRate); delay(10);
  Serial.println();
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData); 
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  delay(1000);
  ax12a.begin(BaudRate, DirectionPin, &Serial);

  int position1 = 0;
  int position2 = 0;
  Serial.println("Starting...");


  LoadCell.begin();
  //LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(1.0); // user set calibration value (float), initial value 1.0 may be used for this sketch
    Serial.println("Startup is complete");
  }
  while (!LoadCell.update());
  calibrate(); //start calibration procedure
}

void loop() {
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      int i = LoadCell.getData();
      
      newDataReady = 0;
      t = millis();
     if (start_new_cycle == true){
        int j = i;
        int loadcell_end_result = j - 185;
        if (loadcell_end_result < 0) {
          Serial.println(loadcell_end_result);
          loadcell_end_result = 0;
        }
        Serial.println(loadcell_end_result);
        String dataString = String(loadcell_end_result);
        String voltageString = String(analogRead(battery_voltage));
        dataString.concat("@");
        dataString.concat(voltageString);
        Serial.println(dataString);
        dataString.toCharArray(buf, 9);
        start_new_cycle = false;
     }
    }
  }

  // receive command from serial terminal
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay(); //tare
    else if (inByte == 'r') calibrate(); //calibrate
    else if (inByte == 'c') changeSavedCalFactor(); //edit calibration value manually
  }

  // check if last tare operation is complete
  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }
}

// callback for sending data
void sendData() {
    Wire.write(buf[index]);
    ++index;   
    if (index >= 9) {
      index = 0;
      start_new_cycle = true; 
    }
}

void calibrate() {
  Serial.println("***");
  Serial.println("Start calibration:");
  Serial.println("Place the load cell an a level stable surface.");
  Serial.println("Remove any load applied to the load cell.");
  Serial.println("Send 't' from serial monitor to set the tare offset.");

  boolean _resume = false;
  while (_resume == false) {
    if (Serial.available() > 0) {
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell.tareNoDelay();
      }
    }
    if (LoadCell.getTareStatus() == true) {
      Serial.println("Tare complete");
      _resume = true;
    }
  }

  Serial.println("Now, place your known mass on the loadcell.");
  Serial.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

  float known_mass = 0;
  _resume = false;
  while (_resume == false) {
    LoadCell.update();
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        Serial.print("Known mass is: ");
        Serial.println(known_mass);
        _resume = true;
      }
    }
  }

  LoadCell.refreshDataSet(); //refresh the dataset to be sure that the known mass is measured correct
  float newCalibrationValue = LoadCell.getNewCalibration(known_mass); //get the new calibration value

  Serial.print("New calibration value has been set to: ");
  Serial.print(newCalibrationValue);
  Serial.println(", use this as calibration value (calFactor) in your project sketch.");
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");

  _resume = false;
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
        start_new_cycle = true;
        only_voltage = false;
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;

      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }

  Serial.println("End calibration");
  Serial.println("***");
  Serial.println("To re-calibrate, send 'r' from serial monitor.");
  Serial.println("For manual edit of the calibration value, send 'c' from serial monitor.");
  Serial.println("***");
}

void changeSavedCalFactor() {
  float oldCalibrationValue = LoadCell.getCalFactor();
  boolean _resume = false;
  Serial.println("***");
  Serial.print("Current value is: ");
  Serial.println(oldCalibrationValue);
  Serial.println("Now, send the new value from serial monitor, i.e. 696.0");
  float newCalibrationValue;
  while (_resume == false) {
    if (Serial.available() > 0) {
      newCalibrationValue = Serial.parseFloat();
      if (newCalibrationValue != 0) {
        Serial.print("New calibration value is: ");
        Serial.println(newCalibrationValue);
        LoadCell.setCalFactor(newCalibrationValue);
        _resume = true;
      }
    }
  }
  _resume = false;
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;
      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }
  Serial.println("End change calibration value");
  Serial.println("***");
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
       ax12a.turn(ID1,LEFT,400);
        ax12a.turn(ID2,RIGHT,400); 
          }
       if(c == 2){

       ax12a.turn(ID1,RIGHT,400);   
       ax12a.turn(ID2,LEFT,400); 
       }
       if(c == 3){
       ax12a.turn(ID3,RIGHT,500);   
       }

    if(c == 4){
       ax12a.turn(ID3,LEFT,600);                  
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
