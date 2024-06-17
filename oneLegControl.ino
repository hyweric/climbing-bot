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
  
}