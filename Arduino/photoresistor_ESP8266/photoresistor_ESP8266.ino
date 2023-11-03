/*
  Title:  Interfacing Photocell or LDR into NodeMCU ESP8266
  Description:  Read LDR or Phot0resistor using ESP8266
  Author: donsky
  For:    www.donskytech.com
  Date:   September 20, 2022
*/

#include <Arduino.h>

int sensorVal = 0;
const int ANALOG_READ_PIN = A0; 

void setup()
{
  Serial.begin(115200);

}

void loop()
{
  sensorVal = analogRead(ANALOG_READ_PIN);

  // Values from 0-1024
  Serial.printf("Light INtensity: %d \n", sensorVal);
//  Serial.printf(sensorVal);

  delay(1000);
}
