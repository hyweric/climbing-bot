#include <Servo.h>

Servo s1;
Servo s2; 
Servo s3;
int servoTargetAdjusted;

void setup() {
  Serial.begin(9600);  
  s2.attach(3);
  s3.attach(10);
  
  smoothWrite(s2, 106, 1);
  smoothWrite(s3, 124, 1);
}

void smoothWrite(Servo servo, int target, int speed) {
  servoTargetAdjusted = map(target, 0, 180, 0, 130); // for some reason the write function needs to be scaled. 
  servo.write(servoTargetAdjusted);
}

void loop() {
  
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    char servoID = input.charAt(0);
    int angle = input.substring(1).toInt();
    Serial.print("s3: ");
    Serial.println(s3.read());

    Serial.print("s2: ");
    Serial.println(s2.read());
  
    switch (servoID) {
      case '2':
        smoothWrite(s2, angle, 10);
        Serial.println("2:" + angle);
        break;
      case '3':
        smoothWrite(s3, angle, 10);
        Serial.println("3:" + angle);
        break;
      default:
        Serial.println("Invalid input");
        break;
    }
  }
}