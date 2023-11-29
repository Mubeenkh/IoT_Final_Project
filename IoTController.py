#!/usr/bin/env python3
#############################################################################
# Filename    : IoTController.py
# Description :	Getting  the RFID tag value and Light Intensity data through the mqtt broker.
# Author      : Mubeen Khan
# modification: 2023/11/26
########################################################################

# pip install paho-mqtt
import paho.mqtt.client as mqtt
from IoTModel import IoTModel
import threading
import time

class IoTController:
    topic_sub1 = "ESP8266/Photoresister"
    topic_sub2 = "ESP8266/RFID" 
    DB_FILE = 'user_data.db'
    user_model = None
    data = 0
    lightIntensity = 0
    rfid = 0

    def __init__(self, broker_address, topic):
        self.user_model = IoTModel(self.DB_FILE)

        self.broker_address = broker_address
        self.topic = topic
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker at {self.broker_address}")
            self.client.subscribe(self.topic)
        else:
            print("Failed to connect, return code: ", rc)

    def on_message(self, client, userdata, message):
        # print(f"{self.topic}: {str(message.payload.decode('utf-8'))}")
        self.data = int(message.payload.decode('utf-8'))

        if(self.topic == "ESP8266/Photoresister"):
            self.lightIntensity = int(message.payload.decode('utf-8'))
            # print(f'Intensity: {self.lightIntensity}')

        if(self.topic == "ESP8266/RFID"):
            self.rfid = int(message.payload.decode('utf-8'))
            # print(f'RFID DATA: {self.rfid}')

    def start(self):
        self.client.connect(self.broker_address, 1883)
        # self.client.loop_forever()
        self.client.loop_start()

    def getData(self):
        # print('------------------------------Light intensity------------------------------')
        # print(self.data) 
        return self.data

    def getLightIntensity(self):
        # print('------------------------------Light intensity------------------------------')
        print(f' Intensity: {self.lightIntensity}')
        return self.lightIntensity
        
    def getRfid(self):
        
        user_info = self.user_model.select_user(self.rfid)
        # print(self.rfid) 
        print(f' User Info: {user_info}')
        user = None
        if(user_info):
            user = {
                'user_id' : user_info[0],
                'user_name' : user_info[1],
                'user_email' : user_info[2],
                'temp_threshold' : user_info[3],
                'hum_threshold' : user_info[4],
                'intensity_threshold' : user_info[5],
            }
        # print(user)
        return user

if __name__ == "__main__":
    broker = "192.168.0.157"
    topic_sub1 = "ESP8266/Photoresister"
    topic_sub2 = "ESP8266/RFID" 

    photoresistor_controller = IoTController(broker, topic_sub1)
    # controller1.start()

    rfid_controller = IoTController(broker, topic_sub2)
    # controller2.start()

    photoresistor_thread = threading.Thread(target=photoresistor_controller.start)
    rfid_thread = threading.Thread(target=rfid_controller.start)
    
    photoresistor_thread.start()
    rfid_thread.start()

    # photoresistor_thread.join()
    # rfid_thread.join()

    while True:

        resistor_value = photoresistor_controller.getLightIntensity()
        if(resistor_value != "" and resistor_value is not None):
            print(f'resistor {resistor_value}')
        
        rfid_value = rfid_controller.getRfid()
        if(rfid_value != "" and rfid_value is not None):
            print(f'rfid {rfid_value}')

        time.sleep(1)
