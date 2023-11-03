  
// To restart mosquitto server: sudo systemctl restart mosquitto

// Get data from publish as a subcribe: mosquitto_sub -t IoTlab/ESP
//  he Topic here is "IoTlab/ESP"

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>

int sensorVal = 0;
const int ANALOG_READ_PIN = A0; 

//const char* ssid ="Gemstelecom08624";
//const char* password ="479202508624";

const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";

//const char* mqtt_server = "mqtt.eclipseprojects.io";
const char* mqtt_server = "192.168.0.157";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

void setup_wifi() {
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP-8266 IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
//    if (client.connect("vanieriot")) {
    if (client.connect("mqtt.eclipseprojects.io")) {
      Serial.println("connected");
    
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      
      // Wait 5 seconds before retrying
      delay(3000);
    }
  }
}

void setup() {

  Serial.begin(115200); 
 
  // Connect to the wifi and to the server
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);

  //print out message
  client.setCallback(callback);
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
    // "IoTlab/ESP" is the topic , while the other is the string body    
    client.publish("IoTlab/ESP","Hello IoTlab");

    sensorVal = analogRead(ANALOG_READ_PIN);
    Serial.printf("Light INtensity: %d \n", sensorVal);
    // Values from 0-1024
    
//    String value = String(sensorVal);
    String s = String(sensorVal);
    client.publish("ESP8266/Photoresister", (char*) s.c_str());

  
  delay(1000);
};
