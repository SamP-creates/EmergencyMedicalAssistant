#include <Servo.h>

Servo leftArm;
Servo rightArm;
Servo testStrips;
Servo claw;

// Sets the angle positions for each of the servo motors
int armStart = 45;
int armEnd = 110;
int delayTime = 20;
int testStrip = 90;
int open = 130;
int close = 180;

// Sets the repeat variable to make sure that the process only occurs once
int repeat = 1;

// Sets the pins for the base of the arm
int basePin1 = 50;
int basePin2 = 51;
int baseSpeed = 12;

void setup() {
  Serial.begin(9600);

  // Connects the pins for the servo motors
  leftArm.attach(40);
  rightArm.attach(42);
  testStrips.attach(43);
  claw.attach(41);

  // Sets the pins as output
  pinMode(basePin1, OUTPUT);
  pinMode(basePin2, OUTPUT);
  pinMode(baseSpeed, OUTPUT);
}

void loop() {
  if (repeat == 1) {
    urineTest();
  } else {
    leftArm.detach();
    rightArm.detach();
    testStrips.detach();
    claw.detach();
  }
}

void urineTest() {
  // Moves the arm up
  for (int angle = armStart; angle <= armEnd; angle++) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  // Opens the claw
  claw.write(open);
  delay(20);

  // Sets the speed of the base
  analogWrite(baseSpeed, 150);

  // Rotates the base of the arm
  digitalWrite(basePin1, HIGH);
  digitalWrite(basePin2, LOW);
  delay(50);

  // Sets the speed of the base
  analogWrite(baseSpeed, 0);

  // Stops the movement of the arm
  digitalWrite(basePin1, LOW);
  digitalWrite(basePin2, LOW);

  // Moves the arm down
  for (int angle = armEnd; angle >= armStart; angle--) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  // Closes the claw to pick up test strip
  for (int clawAngle = open; clawAngle <= close; clawAngle++) {
    claw.write(clawAngle);  // Moves the claw
    delay(delayTime);
  }

  // Moves the arm up
  for (int angle = armStart; angle <= armEnd; angle++) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  // Sets the speed of the base
  analogWrite(baseSpeed, 150);

  // Rotates the base of the arm
  digitalWrite(basePin1, LOW);
  digitalWrite(basePin2, HIGH);
  delay(125);

  // Sets the speed of the base
  analogWrite(baseSpeed, 0);

  // Stops the movement of the arm
  digitalWrite(basePin1, LOW);
  digitalWrite(basePin2, LOW);

  // Moves the arm down
  for (int angle = armEnd; angle >= armStart; angle--) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  delay(4000);

  // Moves the arm up
  for (int angle = armStart; angle <= armEnd; angle++) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  // Sets the speed of the base
  analogWrite(baseSpeed, 150);

  // Rotates the base of the arm
  digitalWrite(basePin1, HIGH);
  digitalWrite(basePin2, LOW);
  delay(35);

  // Sets the speed of the base
  analogWrite(baseSpeed, 0);

  // Stops the movement of the arm
  digitalWrite(basePin1, LOW);
  digitalWrite(basePin2, LOW);

  // Moves the arm down
  for (int angle = armEnd; angle >= armStart; angle--) {
    leftArm.write(angle);                         // Moves the left arm
    rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
    delay(delayTime);
  }

  delay(2000);

  // Opens the claw
  claw.write(open);
  delay(20);

  delay(500);

  // Sets the speed of the base
  analogWrite(baseSpeed, 150);

  // Rotates the base of the arm
  digitalWrite(basePin1, HIGH);
  digitalWrite(basePin2, LOW);
  delay(35);

  // Sets the speed of the base
  analogWrite(baseSpeed, 0);

  // Stops the movement of the arm
  digitalWrite(basePin1, LOW);
  digitalWrite(basePin2, LOW);

  delay(1000);

  repeat = 2;
}