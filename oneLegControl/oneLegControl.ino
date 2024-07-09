#include <Servo.h>

Servo s1;
Servo s2; 
Servo s3;

void setup() {
  Serial.begin(9600);  
  s2.attach(3);
  s3.attach(10);
  
  s2.write(150);
  s3.write(130);
}

void smoothWrite(Servo servo, int target, int speed) {
  servo.write(target);
  // int currentPosition = servo.read();
  // int distance = abs(target - currentPosition);
  // int direction = (target > currentPosition) ? 1 : -1;

  // for (int i = 0; i <= distance; i++) {
  //   int newPosition = currentPosition + (direction * i);
  //   servo.write(newPosition);
  //   delay(speed);
  // }
}

void loop() {
  Serial.print("s2: ");
  Serial.println(s2.read());
  Serial.print("s3: ");
  Serial.println(s3.read());
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    char servoID = input.charAt(0);
    int angle = input.substring(1).toInt();

    switch (servoID) {
      case '1':
        smoothWrite(s1, angle, 10);
        Serial.println("1:" + angle);
        break;
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
