#include <Servo.h>

Servo s1;
Servo s2; 
Servo s3;

void setup() {
  Serial.begin(9600); 
  s1.attach(3); 
  s2.attach(9);
  s3
.attach(10);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    char servoID = input.charAt(0);
    int angle = input.substring(1).toInt();

    switch (servoID) {
      case '1':
        s1.write(angle);
        Serial.println("1:" + angle);
        break;
      case '2':
        s2.write(angle);
        Serial.println("2:" + angle);
        break;
      case '3':
        s3
      .write(angle);
        Serial.println("3:" + angle);
        break;
      default:
        Serial.println("Invalid input");
        break;
    }
  }
}