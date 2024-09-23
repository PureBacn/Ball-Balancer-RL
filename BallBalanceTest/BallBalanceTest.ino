#include "TouchScreen.h"
#include <InverseKinematics.h>
#include <AccelStepper.h>

// Define your Touch screen connections
#define X1 A0
#define X2 A2
#define Y1 A3
#define Y2 A1

#define maxSpeed 1000
#define maxAccel 1000

TouchScreen ts = TouchScreen(X1, Y1, X2, Y2, 0);

AccelStepper stepper1(AccelStepper::DRIVER, 2, 5);
AccelStepper stepper2(AccelStepper::DRIVER, 3, 6);
AccelStepper stepper3(AccelStepper::DRIVER, 4, 7);

Machine machine(2, 3.125, 1.75, 3.669291339);

void setup() {
  Serial.begin(9600);

  // Initialize Stepper 1
  stepper1.setEnablePin(4);
  stepper1.setCurrentPosition(0);
  stepper1.setMaxSpeed(maxSpeed);      // Set the max speed without large scaling
  stepper1.setAcceleration(maxAccel);  // Set the acceleration

  // Initialize Stepper 2
  stepper2.setCurrentPosition(0);
  stepper2.setMaxSpeed(maxSpeed);      // Set the max speed without large scaling
  stepper2.setAcceleration(maxAccel);  // Set the acceleration

  // Initialize Stepper 3
  stepper3.setCurrentPosition(0);
  stepper3.setMaxSpeed(maxSpeed);      // Set the max speed without large scaling
  stepper3.setAcceleration(maxAccel);  // Set the acceleration

  // Set movement target to a reasonable value (200 steps in this case)
  stepper1.moveTo(200); 
  stepper2.moveTo(200);
  stepper3.moveTo(200);
}

void loop() {
  // Read from the touchscreen
  TSPoint p = ts.getPoint();
  Serial.print((p.x - 100.0) / 810.0);
  Serial.print(" ");
  Serial.println((p.y - 90.0) / 850.0);

  do {
    // Run the steppers
    stepper1.run();
    stepper2.run();
    stepper3.run();
    delay(100);
  } while (Serial.available() < 0);
  
  String x = Serial.readString();
  x.trim();
  x = x.toFloat();
  String z = Serial.readString();
  z.trim();
  z = z.toFloat();

  
}
