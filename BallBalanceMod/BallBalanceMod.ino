//***3RPS Parallel Manipulator Ball Balancer Code BY Aaed Musa**
//--------------------------------------------------------------

//libraries
#include <AccelStepper.h>
#include <InverseKinematics.h>
#include <MultiStepper.h>
#include <stdint.h>
#include <TouchScreen.h>
#include <math.h>

Machine machine(2, 3.125, 1.75, 3.669291339);     //(d, e, f, g) object to define the lengths of the machine
TouchScreen ts = TouchScreen(A2, A3, A0, A1, 0);  //touch screen pins (XGND, YGND, X5V, Y5V)
/*
TouchScreen ts = TouchScreen(A1, A0, A3, A2, 0);  //touch screen pins (XGND, YGND, X5V, Y5V)
*/

//stepper motors

AccelStepper stepperA(AccelStepper::DRIVER, 2, 5);
AccelStepper stepperB(AccelStepper::DRIVER, 3, 6);
AccelStepper stepperC(AccelStepper::DRIVER, 4, 7);

/*
AccelStepper stepperA(1, 1, 2);  //(driver type, STEP, DIR) Driver A
AccelStepper stepperB(1, 3, 4);  //(driver type, STEP, DIR) Driver B
AccelStepper stepperC(1, 5, 6);  //(driver type, STEP, DIR) Driver C
*/

MultiStepper steppers;           // Create instance of MultiStepper

/*
//PID variables
double kp = 4E-4, ki = 2E-6, kd = 7E-3;                                                       //PID constants
double error[2] = { 0, 0 }, errorPrev[2], integr[2] = { 0, 0 }, deriv[2] = { 0, 0 }, out[2];  //PID terms for X and Y directions
long timeI;                                                                           //variables to capture initial times
*/

double out[2];
long timeI;
const byte datasize = 41;
char storeddata[datasize];
boolean newdata = false;

//stepper motor variables
long pos[3];                                            // An array to store the target positions for each stepper motor
int ENA = 4;                                           //enable pin for the drivers
double angOrig = 206.662752199;                        //original angle that each leg starts at
double speed[3] = { 0, 0, 0 }, speedPrev[3], ks = 20;  //the speed of the stepper motor and the speed amplifying constant                                                                         //variables to capture initial times

//Other Variables
double angToStep = 3200 / 360;  //angle to step conversion factor (steps per degree) for 16 microsteps or 3200 steps/rev
bool detected = 0;              //this value is 1 when the ball is detected and the value is 0 when the ball in not detected

void setup() {
  Serial.begin(115200);

  //Set stepper max speeds
  stepperA.setMaxSpeed(200);
  stepperB.setMaxSpeed(200);
  stepperC.setMaxSpeed(200);
  
  // Adding the steppers to the steppersControl instance for multi stepper control
  steppers.addStepper(stepperA);
  steppers.addStepper(stepperB);
  steppers.addStepper(stepperC);
  
  //Enable pin
  pinMode(ENA, OUTPUT);           //define enable pin as output
  digitalWrite(ENA, HIGH);        //sets the drivers off initially
  delay(1000);                    //small delay to allow the user to reset the platform
  digitalWrite(ENA, LOW);         //sets the drivers on
  moveTo(4.25, 0, 0);             //moves the platform to the home position
  steppers.runSpeedToPosition();  //blocks until the platform is at the home position
}
void loop() {
  //PID(0.5, 0.5);  //(X setpoint, Y setpoint) -- must be looped
  Shift();
}
void moveTo(double hz, double nx, double ny) {
  //if the ball has been detected
  if (detected) {
    //calculates stepper motor positon
    for (int i = 0; i < 3; i++) {
      pos[i] = round((angOrig - machine.theta(i, hz, nx, ny)) * angToStep);
    }
    //sets calculated speed
    stepperA.setMaxSpeed(speed[A]);
    stepperB.setMaxSpeed(speed[B]);
    stepperC.setMaxSpeed(speed[C]);
    //sets acceleration to be proportional to speed
    stepperA.setAcceleration(speed[A] * 30);
    stepperB.setAcceleration(speed[B] * 30);
    stepperC.setAcceleration(speed[C] * 30);
    //sets target positions
    stepperA.moveTo(pos[A]);
    stepperB.moveTo(pos[B]);
    stepperC.moveTo(pos[C]);
    //runs stepper to target position (increments at most 1 step per call)
    stepperA.run();
    stepperB.run();
    stepperC.run();
  }
  //if the hasn't been detected
  else {
    for (int i = 0; i < 3; i++) {
      pos[i] = round((angOrig - machine.theta(i, hz, 0, 0)) * angToStep);
    }
    //sets max speed
    stepperA.setMaxSpeed(800);
    stepperB.setMaxSpeed(800);
    stepperC.setMaxSpeed(800);
    //moves the stepper motors
    steppers.moveTo(pos);
    steppers.run();  //runs stepper to target position (increments at most 1 step per call)
  }
}

void setData(String data){
  String x;
  String z;
  while (data.length() > 0)
  {
    int index = data.indexOf(" ");
    if (index == -1)
    {
        z = data;
        break;
    }
    else
    {
      x = data.substring(0,index);
      data = data.substring(index+1);
    }
  }

  out[0] = x.toDouble();
  out[1] = z.toDouble();
}

void receivedata() {
  static byte index = 0;
  char endmarker = '\n';
  char read;
  //Serial.println("Received Data");
  while (Serial.available() > 0 && !newdata) {
    read = Serial.read();
   
    if (read != endmarker) {
      storeddata[index] = read;
      index++;
      if (index >= datasize) {
        index = datasize - 1;
      }
    }
    else {
      //storeddata[index] = "\0";
      index = 0;
      newdata = true;
    }
  }
}


//takes in an X and Y setpoint/position and moves the ball to that position
void Shift() { //PID(double setpointX, double setpointY) {
  TSPoint p = ts.getPoint();  //measure X and Y positions
  //if the ball is detected (the x position will not be 0)
  if (p.x != 0) {
    detected = 1;
    Serial.print((p.x - 100.0) / 810.0);
    Serial.print(" ");
    Serial.println((p.y - 90.0) / 850.0);

    receivedata();
    if (newdata) {
      char data[strlen(storeddata) + 1];
      strcpy(data, storeddata);
      setData(String(data));
      newdata = false;
    }

    for (int i = 0; i < 3; i++) {
      speedPrev[i] = speed[i];                                                                                                           //sets previous speed
      speed[i] = (i == A) * stepperA.currentPosition() + (i == B) * stepperB.currentPosition() + (i == C) * stepperC.currentPosition();  //sets current position
      speed[i] = abs(speed[i] - pos[i]) * ks;                                                                                            //calculates the error in the current position and target position
      speed[i] = constrain(speed[i], speedPrev[i] - 200, speedPrev[i] + 200);                                                            //filters speed by preventing it from beign over 100 away from last speed
      speed[i] = constrain(speed[i], 0, 1000);                                                                                           //constrains sped from 0 to 1000
    }
  }
  //if the ball is not detected (the x value will be 0)
  else {
    //double check that there is no ball
    delay(10);                  //10 millis delay before another reading
    TSPoint p = ts.getPoint();  //measure X and Y positions again to confirm no ball
    if (p.x == 0) {             //if the ball is still not detected
      detected = 0;
    }
  }
  moveTo(4.25, -out[0], -out[1]);
  /*
  //continues moving platform and waits until 20 millis has elapsed
  timeI = millis();
  while (millis() - timeI < 20) {
    moveTo(4.25, out[0], out[1]);  //moves the platfrom
  }
  */
}

/*      POV: You Work At Google
⣿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⢻⣿⣿⡇
⣿⡆⠊⠈⣿⢿⡟⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣎⠈⠻⣿⡇
⣿⣷⣠⠁⢀⠰⠀⣰⣿⣿⣿⣿⣿⣿⠟⠋⠛⠛⠿⠿⢿⣿⣿⣿⣧⠀⢹⣿⡑⠐ ⣿⣿
⣿⣿⣿⠀⠁⠀⠀⣿⣿⣿⣿⠟⡩⠐⠀⠀⠀⠀⢐⠠⠈⠊⣿⣿⣿⡇⠘⠁⢀⠆⢀⣿⣿⡇
⣿⣿⣿⣆⠀⠀⢤⣿⣿⡿⠃⠈⠀⣠⣶⣿⣿⣷⣦⡀⠀⠀⠈⢿⣿⣇⡆⠀⠀⣠⣾⣿⣿⡇
⣿⣿⣿⣿⣧⣦⣿⣿⣿⡏⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠐⣿⣿⣷⣦⣷⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⣾⣿⣿⠋⠁⠀⠉⠻⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⡿⠁⠀⠀⠀⠀⠀⠘⢿⣿⠀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣠⣂⠀⠀⠀⠀⠀⠀⠀⢀⣁⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⣤⣤⣔⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
 */
