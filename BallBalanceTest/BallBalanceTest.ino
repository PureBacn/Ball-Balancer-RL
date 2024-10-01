#include "TouchScreen.h"
TouchScreen ts = TouchScreen(A2, A3, A0, A1, 0);

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Read from the touchscreen
  TSPoint p = ts.getPoint();
  /*
  Serial.print(p.x);
  Serial.print(" ");
  Serial.println(p.y);
  */
  Serial.print((p.x - 75.0) / 835.0);
  Serial.print(" ");
  Serial.println((p.y - 150.0) / 695.0);
}
