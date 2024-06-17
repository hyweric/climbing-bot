#include <Servo.h>

Servo hip;
Servo knee;
Servo abad;

const int hipPin = 3;
const int kneePin = 5;
const int abadPin = 10;

void setup() {
  Serial.begin(9600);
  
  hip.attach(hipPin);
  knee.attach(kneePin);
  abad.attach(abadPin);
}

void loop() {
  if (Serial.available()) {
    char servoId = Serial.read();
    if (Serial.read() == ':') {
      int pos = Serial.parseInt();
      switch (servoId) {
        case '1':
          hip.write(pos);
          break;
        case '2':
          knee.write(pos);
          break;
        case '3':
          abad.write(pos);
          break;
      }
    }
  }
}