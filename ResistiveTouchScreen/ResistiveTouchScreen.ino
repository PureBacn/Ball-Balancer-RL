/*=================================
  This code demostrates 4-Wire Touch screen
  interfacing with Arduino

  blog.circuits4you.com
  www.circuits4you.com

  4- Wire Touchscreen Connections
  A0=====X+
  A1=====X-
  A2=====Y+
  A3=====Y-
  =================================*/

#include <Stepper.h>

  
//Define your Touch screen connections
#define X1 A0
#define X2 A1
#define Y1 A2
#define Y2 A3
//Define your screen resolution as per your Touch screen (Max: 1024)
#define Xresolution 320 //128
#define Yresolution 240 //64

#define FULLSTEP 8


float angles[3];

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int X, Y; //Touch Coordinates are stored in X,Y variable
  pinMode(Y1, INPUT);
  pinMode(Y2, INPUT);
  digitalWrite(Y2, LOW);
  pinMode(X1, OUTPUT);
  digitalWrite(X1, HIGH);
  pinMode(X2, OUTPUT);
  digitalWrite(X2, LOW);
  X = (analogRead(Y1)) / (1024 / Xresolution); //Reads X axis touch position

  pinMode(X1, INPUT);
  pinMode(X2, INPUT);
  digitalWrite(X2, LOW);
  pinMode(Y1, OUTPUT);
  digitalWrite(Y1, HIGH);
  pinMode(Y2, OUTPUT);
  digitalWrite(Y2, LOW);
  Y = (analogRead(X1)) / (1024 / Yresolution); //Reads Y axis touch position

  //Display X and Y on Serial Monitor
  Serial.print(X);
  Serial.print(" ");
  Serial.println(Y);
  delay(100);

  while (Serial.available() < 0) {
    delay(100);
  }
  String a0 = Serial.readString();
  a0.trim();
  angles[0] = a0.toFloat();
  String a1 = Serial.readString();
  a1.trim();
  angles[1] = a1.toFloat();
  String a2 = Serial.readString();
  a2.trim();
  angles[2] = a2.toFloat();
  Serial.println(a0 + " " + a1 + " " + a2);
}
