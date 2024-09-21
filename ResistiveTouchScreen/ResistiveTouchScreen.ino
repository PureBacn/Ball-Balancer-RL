#include "TouchScreen.h"
#include <AccelStepper.h>

//Define your Touch screen connections
#define X1 A0
#define X2 A2
#define Y1 A3
#define Y2 A1

TouchScreen ts = TouchScreen(X1,Y1,X2,Y2,0);
AccelStepper stepper(AccelStepper::DRIVER, 2, 5);

void setup()
{
   Serial.begin(9600);
   pinMode(4,OUTPUT);
    stepper.setMaxSpeed(200);      // Set desired speed
    stepper.setAcceleration(100);   // Set acceleration
    stepper.moveTo(10000);
}

void loop()
{
  TSPoint p = ts.getPoint();
  Serial.print((p.x-100.0)/810.0);
  Serial.print(" ");
  Serial.println((p.y-90.0)/850.0);
  stepper.runSpeed();
}
