  
// To restart mosquitto server: sudo systemctl restart mosquitto

// Get data from publish as a subcribe: mosquitto_sub -t IoTlab/ESP
//  he Topic here is "IoTlab/ESP"

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN D8
#define RST_PIN D0


//MFRC522 by GithubCommunity
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;

// Init array that will store new NUID
byte nuidPICC[4];

int sensorVal = 0;
const int ANALOG_READ_PIN = A0; 

//const char* ssid ="Muffins Hut";
//const char* password ="Muffin22";
//const char* mqtt_server = "172.20.10.3";

const char* ssid ="Gemstelecom08624";
const char* password ="479202508624";

//const char* ssid = "TP-Link_2AD8";
//const char* password = "14730078";
const char* mqtt_server = "192.168.0.157";

//const char* ssid = "VIRGIN389";
//const char* password = "A9D5164D6C25";
//const char* mqtt_server = "192.168.2.40";



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


String getDecID(byte *buffer, byte bufferSize) {
  String dec = "";   

  for (byte i = 0; i < bufferSize; i++) {
    dec += buffer[i], DEC;
  }
  Serial.println(dec);

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  
  return dec;
}




void setup() {

  Serial.begin(115200); 
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
 
  // Connect to the wifi and to the server
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);

  //print out message
  client.setCallback(callback);
  
}


void loop() {

  delay(1000);
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");
    
  // "IoTlab/ESP" is the topic , while the other is the string body    
  client.publish("IoTlab/ESP","Hello IoTlab");

// Light intensity
  sensorVal = analogRead(ANALOG_READ_PIN);
  
  Serial.printf("Light Intensity: %d \n", sensorVal);
  // Values from 0-1024
  String s = String(sensorVal);
  client.publish("ESP8266/Photoresister", (char*) s.c_str());

// RFID
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
   if ( ! rfid.PICC_ReadCardSerial())
     return;

  String rfid_tag = getDecID(rfid.uid.uidByte, rfid.uid.size);
  client.publish("ESP8266/RFID",rfid_tag.c_str());

}
