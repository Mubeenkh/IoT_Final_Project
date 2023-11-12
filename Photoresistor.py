#!/usr/bin/env python3
#############################################################################
# Filename    : Photoresistor.py
# Description :	Getting  for Light Intensity data from Photoresistor using MQTT.
#               Data is comming from ESP8266.
# Author      : Mubeen Khan
# modification: 2023/11/03
########################################################################

# pip install paho-mqtt
import paho.mqtt.client as mqtt

class Photoresistor:
	
    topic_sub = "ESP8266/Photoresister" 
    # broker_address = "mqtt.eclipseprojects.io"
    broker_address = "192.168.0.157"
    # broker_address = "192.168.2.40"

    lightIntensity = 0
    
    def __init__(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))

            client.subscribe(self.topic_sub)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):

            # print('------------------------------Light intensity------------------------------')
            # print(msg.topic+": "+str(msg.payload.decode("utf-8")))
            self.lightIntensity = int(msg.payload.decode("utf-8"))

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(self.broker_address, 1883, 60)
        client.loop_start()


    def getLightIntensity(self):
        # print('------------------------------Light intensity------------------------------')
        # print(self.lightIntensity)
        return self.lightIntensity
