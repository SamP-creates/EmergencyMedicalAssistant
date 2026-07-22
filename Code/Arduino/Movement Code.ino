#include "Adafruit_VL53L0X.h"

// Creates the five time-of-flight sensors
Adafruit_VL53L0X frontTOF = Adafruit_VL53L0X();
Adafruit_VL53L0X leftTOF = Adafruit_VL53L0X();
Adafruit_VL53L0X backTOF = Adafruit_VL53L0X();
Adafruit_VL53L0X rightTOF = Adafruit_VL53L0X();
Adafruit_VL53L0X upTOF = Adafruit_VL53L0X();
Adafruit_VL53L0X downTOF = Adafruit_VL53L0X();

// Sets the drivetrain motor pins
int leftPin1 = 24;
int leftPin2 = 25;
int rightPin1 = 26;
int rightPin2 = 27;
int leftSpeedPin = 11;
int rightSpeedPin = 10;

// Sets the rack motor pins
int leftRackPin1 = 32;
int leftRackPin2 = 33;
int rightRackPin1 = 34;
int rightRackPin2 = 35;
int leftRackSpeedPin = 9;
int rightRackSpeedPin = 9;

// Function to select I2C BUS
void TCA9548A(uint8_t bus) {
  Wire.beginTransmission(0x70);  //TCA9548A address
  Wire.write(1 << bus);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);  // Sets the baud rate for the serial monitor

  Wire.begin();

  // Booting front time-of-flight sensor
  TCA9548A(0);              // Runs the function to call the sensor SDA and SCL pins
  if (!frontTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot front ToF"));
    while (1)
      ;
  }
  Serial.println("Booted front ToF");


  // Booting right time-of-flight sensor
  TCA9548A(1);             // Runs the function to call the sensor SDA and SCL pins
  if (!rightTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot right ToF"));
    while (1)
      ;
  }
  Serial.println("Booted right ToF");

  // Booting back time-of-flight sensor
  TCA9548A(7);             // Runs the function to call the sensor SDA and SCL pins
  if (!backTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot back ToF"));
    while (1)
      ;
  }
  Serial.println("Booted back ToF");

  // Booting left time-of-flight sensor
  TCA9548A(3);              // Runs the function to call the sensor SDA and SCL pins
  if (!leftTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot left ToF"));
    while (1)
      ;
  }
  Serial.println("Booted left ToF");

  // Booting up time-of-flight sensor
  TCA9548A(4);           // Runs the function to call the sensor SDA and SCL pins
  if (!upTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot up ToF"));
    while (1)
      ;
  }
  Serial.println("Booted up ToF");

  // Booting down time-of-flight sensor
  TCA9548A(5);             // Runs the function to call the sensor SDA and SCL pins
  if (!downTOF.begin()) {  // If the ToF sensor is not working
    Serial.println(F("Failed to boot down ToF"));
    while (1)
      ;
  }
  Serial.println("Booted down ToF");

  // Sets the mode for the drivetrain pins
  pinMode(leftPin1, OUTPUT);
  pinMode(leftPin2, OUTPUT);
  pinMode(rightPin1, OUTPUT);
  pinMode(rightPin2, OUTPUT);

  pinMode(leftSpeedPin, OUTPUT);
  pinMode(rightSpeedPin, OUTPUT);

  // Sets the mode for the rack pins
  pinMode(leftRackPin1, OUTPUT);
  pinMode(leftRackPin2, OUTPUT);
  pinMode(rightRackPin1, OUTPUT);
  pinMode(rightRackPin2, OUTPUT);

  pinMode(leftRackSpeedPin, OUTPUT);
  pinMode(rightRackSpeedPin, OUTPUT);
}

void turnToPerson(int speed) {
  // Gets the measurements from the front time-of-flight sensor
  TCA9548A(0);
  VL53L0X_RangingMeasurementData_t frontMeasure;
  frontTOF.rangingTest(&frontMeasure, false);

  // Gets the measurements from the right time-of-flight sensor
  TCA9548A(1);
  VL53L0X_RangingMeasurementData_t rightMeasure;
  rightTOF.rangingTest(&rightMeasure, false);

  //Gets the measurements from the back time-of-flight sensor
  TCA9548A(7);
  VL53L0X_RangingMeasurementData_t backMeasure;
  backTOF.rangingTest(&backMeasure, false);

  // Gets the measurements from the left time-of-flight sensor
  TCA9548A(3);
  VL53L0X_RangingMeasurementData_t leftMeasure;
  leftTOF.rangingTest(&leftMeasure, false);

  // Checks if the robot is facing the patient
  if (frontMeasure.RangeMilliMeter <= 500) {
    Serial.println("patient in front");
    analogWrite(leftSpeedPin, 0);
    analogWrite(rightSpeedPin, 0);

    // Stops the movement for both the left and right motor pairs
    digitalWrite(leftPin1, LOW);
    digitalWrite(leftPin2, LOW);

    digitalWrite(rightPin1, LOW);
    digitalWrite(rightPin2, LOW);

    // Calls the function to make the robot lift the rack
    changeHeight(200);
  }
  // Checks if a patient is on the right side of the robot
  else if (rightMeasure.RangeMilliMeter <= 500) {
    Serial.println("turn left");
    analogWrite(leftSpeedPin, speed);
    analogWrite(rightSpeedPin, speed);

    // Turns the robot to the right
    digitalWrite(leftPin1, LOW);
    digitalWrite(leftPin2, HIGH);

    digitalWrite(rightPin1, HIGH);
    digitalWrite(rightPin2, LOW);
  }
  // Checks if a patient is on the left side of the robot
  else if (leftMeasure.RangeMilliMeter <= 500) {
    Serial.println("turn right");
    analogWrite(leftSpeedPin, speed);
    analogWrite(rightSpeedPin, speed);

    // Turns the robot to the left
    digitalWrite(leftPin1, HIGH);
    digitalWrite(leftPin2, LOW);

    digitalWrite(rightPin1, LOW);
    digitalWrite(rightPin2, HIGH);
  }
  // Checks if a patient is at the back of the robot
  else if (backMeasure.RangeMilliMeter <= 500) {
    Serial.println("turn front");
    analogWrite(leftSpeedPin, speed);
    analogWrite(rightSpeedPin, speed);

    // Makes the robot turn until in front of the robot
    digitalWrite(leftPin1, HIGH);
    digitalWrite(leftPin2, LOW);

    digitalWrite(rightPin1, LOW);
    digitalWrite(rightPin2, HIGH);
  }
  // Checks if no patient is near the robot
  else {
    Serial.println("don't move anywhere");
    analogWrite(leftSpeedPin, 0);
    analogWrite(rightSpeedPin, 0);

    // Stops the movement for both the left and right motor pairs
    digitalWrite(leftPin1, LOW);
    digitalWrite(leftPin2, LOW);

    digitalWrite(rightPin1, LOW);
    digitalWrite(rightPin2, LOW);
  }
}

void changeHeight(int liftSpeed) {
  // Gets the measurements from the up time-of-flight sensor
  TCA9548A(4);
  VL53L0X_RangingMeasurementData_t upMeasure;
  upTOF.rangingTest(&upMeasure, false);

  // Gets the measurements from the down time-of-flight sensor
  TCA9548A(5);
  VL53L0X_RangingMeasurementData_t downMeasure;
  downTOF.rangingTest(&downMeasure, false);

  // Checks if the patient is trying to lift up the rack
  if (upMeasure.RangeMilliMeter <= 200) {
    Serial.println("Raising");

    analogWrite(leftRackSpeedPin, liftSpeed);
    analogWrite(rightRackSpeedPin, liftSpeed);

    // Moves all of the racks up
    digitalWrite(leftRackPin1, LOW);
    digitalWrite(leftRackPin2, HIGH);
    digitalWrite(rightRackPin1, LOW);
    digitalWrite(rightRackPin2, HIGH);
  }
  // Checks if the patient is trying to lower the rack
  else if (downMeasure.RangeMilliMeter <= 200) {
    Serial.println("Lowering");

    // Sets the speed to lower the rack
    analogWrite(leftRackSpeedPin, liftSpeed);
    analogWrite(rightRackSpeedPin, liftSpeed);

    // Moves all of the racks down
    digitalWrite(leftRackPin1, HIGH);
    digitalWrite(leftRackPin2, LOW);
    digitalWrite(rightRackPin1, HIGH);
    digitalWrite(rightRackPin2, LOW);
  }
  // Checks if the patient is putting both sides
  else if (downMeasure.RangeMilliMeter <= 200 && upMeasure.RangeMilliMeter <= 200) {
    // Sets the speed to zero
    analogWrite(leftRackSpeedPin, 0);
    analogWrite(rightRackSpeedPin, 0);

    // Stops the motors
    digitalWrite(leftRackPin1, LOW);
    digitalWrite(leftRackPin2, LOW);
    digitalWrite(rightRackPin1, LOW);
    digitalWrite(rightRackPin2, LOW);
  } else {
    // Sets the speed to zero
    analogWrite(leftRackSpeedPin, 0);
    analogWrite(rightRackSpeedPin, 0);

    // Stops the motors
    digitalWrite(leftRackPin1, LOW);
    digitalWrite(leftRackPin2, LOW);
    digitalWrite(rightRackPin1, LOW);
    digitalWrite(rightRackPin2, LOW);
  }
}

void loop() {
  turnToPerson(225);
}



// #include <Servo.h>

// Servo leftArm;
// Servo rightArm;
// Servo testStrips;
// Servo claw;

// // Sets the angle positions for each of the servo motors
// int armStart = 45;
// int armEnd = 110;
// int delayTime = 20;
// int testStrip = 90;
// int open = 130;
// int close = 180;

// // Sets the repeat variable to make sure that the process only occurs once
// int repeat = 1;

// // Sets the pins for the base of the arm
// int basePin1 = 50;
// int basePin2 = 51;
// int baseSpeed = 12;

// void setup() {
//   Serial.begin(9600);

//   // Connects the pins for the servo motors
//   leftArm.attach(40);
//   rightArm.attach(42);
//   testStrips.attach(43);
//   claw.attach(41);

//   // Sets the pins as output
//   pinMode(basePin1, OUTPUT);
//   pinMode(basePin2, OUTPUT);
//   pinMode(baseSpeed, OUTPUT);
// }

// void loop() {
//   if (repeat == 1) {
//     urineTest();
//   } else {
//     leftArm.detach();
//     rightArm.detach();
//     testStrips.detach();
//     claw.detach();
//   }
// }

// void urineTest() {
//   // Moves the arm up
//   for (int angle = armStart; angle <= armEnd; angle++) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   // Opens the claw
//   claw.write(open);
//   delay(20);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 150);

//   // Rotates the base of the arm
//   digitalWrite(basePin1, HIGH);
//   digitalWrite(basePin2, LOW);
//   delay(50);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 0);

//   // Stops the movement of the arm
//   digitalWrite(basePin1, LOW);
//   digitalWrite(basePin2, LOW);

//   // Moves the arm down
//   for (int angle = armEnd; angle >= armStart; angle--) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   // Closes the claw to pick up test strip
//   for (int clawAngle = open; clawAngle <= close; clawAngle++) {
//     claw.write(clawAngle);  // Moves the claw
//     delay(delayTime);
//   }

//   // Moves the arm up
//   for (int angle = armStart; angle <= armEnd; angle++) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 150);

//   // Rotates the base of the arm
//   digitalWrite(basePin1, LOW);
//   digitalWrite(basePin2, HIGH);
//   delay(125);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 0);

//   // Stops the movement of the arm
//   digitalWrite(basePin1, LOW);
//   digitalWrite(basePin2, LOW);

//   // Moves the arm down
//   for (int angle = armEnd; angle >= armStart; angle--) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   delay(4000);

//   // Moves the arm up
//   for (int angle = armStart; angle <= armEnd; angle++) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 150);

//   // Rotates the base of the arm
//   digitalWrite(basePin1, HIGH);
//   digitalWrite(basePin2, LOW);
//   delay(35);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 0);

//   // Stops the movement of the arm
//   digitalWrite(basePin1, LOW);
//   digitalWrite(basePin2, LOW);

//   // Moves the arm down
//   for (int angle = armEnd; angle >= armStart; angle--) {
//     leftArm.write(angle);                         // Moves the left arm
//     rightArm.write(armEnd - (angle - armStart));  // Moves the right arm in the opposite direction
//     delay(delayTime);
//   }

//   delay(2000);

//   // Opens the claw
//   claw.write(open);
//   delay(20);

//   delay(500);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 150);

//   // Rotates the base of the arm
//   digitalWrite(basePin1, HIGH);
//   digitalWrite(basePin2, LOW);
//   delay(35);

//   // Sets the speed of the base
//   analogWrite(baseSpeed, 0);

//   // Stops the movement of the arm
//   digitalWrite(basePin1, LOW);
//   digitalWrite(basePin2, LOW);

//   delay(1000);

//   repeat = 2;
// }
