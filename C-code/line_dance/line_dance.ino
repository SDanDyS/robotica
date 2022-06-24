// FFT
#include <fix_fft.h>

char im[128], data[128];
char x = 0, ylim = 60;
int i = 0, val;
int beatHight = 30;
int beats = 0;
unsigned int beatStartValue = 350;
unsigned int beatTime = 0;
unsigned int beatTiming = 0;
unsigned int beatDelay = beatStartValue;
unsigned long start = 0;
unsigned long end = 0;

#define microphone (0u)
//#define microphone A6
#define baudRate (9600u)
#define DC_OFFSET 15
#define NOISE 18
#define TOP 32

const int sampleWindow = 50; // Sample window width in ms (50 ms = 20Hz)
unsigned int sample;

int lvl = 20;

// For dynamic adjustment of graph low & high
int minLvlAvg = 0; 
int maxLvlAvg = 512;

float mapFloat(int value, float fromLow, float fromHigh, float toLow, float toHigh) {
  float fraction = (value - fromLow) / (fromHigh - fromLow);
  return fraction * (toHigh - toLow) + toLow;
}

void setup() {
  Serial.begin(baudRate);
//  pinMode(microphone, OUTPUT);
//  analogReference(DEFAULT);
}

void calculateP2p(){
  unsigned long startMillis = millis();
  unsigned int peakToPeak = 0;

  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;
  
  while(millis() - startMillis < sampleWindow){    
    int micValue = analogRead(microphone);
    
    // Filter on spurious reading
    if(micValue < 1024){
      if(micValue > signalMax){
        signalMax = micValue;
      } else if (micValue < signalMin){
        signalMin = micValue;
      }
    }

    peakToPeak = signalMax - signalMin;
    Serial.println(peakToPeak);
  }
}

void getOutput(int delayTime = 0){
  uint16_t minLvl, maxLvl;
  int height;
  
  int micValue = analogRead(microphone); // Raw reading from mic
  micValue = abs(micValue - 512 - DC_OFFSET); // Center on zero
  micValue= (micValue <= NOISE) ? 0 : (micValue - NOISE); // Remove noise/hum
  lvl = ((lvl * 7) + micValue) >> 3; // "Dampened" reading (else looks twitchy)

  // Calculate bar height based on dynamic min/max levels (fixed point):
  height = TOP * (lvl - minLvlAvg) / (long)(maxLvlAvg - minLvlAvg);
  
  Serial.println(micValue);
  delay(delayTime);
}

void getVUMeter(){
  int samples = 5;
  float offset = 336;
  int readings = 0;
  
  
  for (int i = 0; i < samples; i++) {
    int micValue = analogRead(microphone);
    readings += micValue;
  }

  float average = readings / samples;
  average -= offset;

  if (average >= beatHight) {
    beatDetected();
  }
//  micValue = micValue/10;
//  float analogvalue = mapFloat(micValue, 0, 1023, 2.4, 5.5);
//  Serial.println(average);

}

void beatDetected(){
  beats++;

  if (start == 0){
    start = millis();
  } else {
    end = millis();
    beatTime = end - start;
    start = 0;
    end = 0;
  }

//  Serial.println(beats);
  delay(beatDelay);
  
  if (beatDelay == beatStartValue || beatDelay < 30){
    beatDelay = beatTime * 0.9;
    beatTiming = beatTime;
  } else if (beatTime < beatDelay) {
    beatDelay = beatTime * 0.9;
    beatTiming = beatTime;
  } else if (beatTime > (beatDelay * 1.05) && beatTime < (beatDelay * 1.45)) {
    beatDelay = beatTime * 0.9;
    beatTiming = beatTime;
  }
  
//  Serial.print("beatTiming:");
//  Serial.print(beatTiming);
//  Serial.print(",");
//  Serial.print("beatDelay:");
//  Serial.print(beatDelay);
//  Serial.print(",");
//  Serial.print("beatTime:");
//  Serial.println(beatTime);
}

void FFT() {
  const int hzRange = 3;
  int min = 1024, max = 0;
  
  for (i = 0; i < 128; i++) {
    val = analogRead(microphone);
    data[i] = val / 4 - 128;
//    Serial.println(val);
    im[i] = 0;
    if(val > max) max = val;
    if(val < min) min = val;
  }

//  Serial.print("max:");
//  Serial.println(max);

  fix_fft(data, im, 1000, 0);

  for(i = 0; i <= hzRange; i++){
    int dat = sqrt(data[i] * data[i] + im[i] * im[i]); // Filter out noise and hum
    
    if(i != hzRange){
      Serial.print(String(i) + ":");
      Serial.print(dat);
      Serial.print(",");
    } else {
      Serial.println(dat);
    }
  }
//  delay(100);
}


void loop() {
//  calculateP2p();
//  getOutput();
  getVUMeter();
//  FFT();
}
