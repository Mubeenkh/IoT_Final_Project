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
from IoTModel import IoTModel
import threading
import time
# class IoTController:
	
#     topic_sub1 = "ESP8266/Photoresister"
#     topic_sub2 = "ESP8266/RFID" 
#     topic = ""
#     # broker_address = "192.168.0.157"
#     # broker_address = "172.20.10.2"    
#     broker_address = "192.168.2.40"

#     lightIntensity = 0
#     rfid = 0

#     lightIntensity = 0
#     data = 0
    
#     DB_FILE = 'user_data.db'
#     user_model = None
    
#     def __init__(self):
#         print('Viewing User Model')
#         self.user_model = IoTModel(self.DB_FILE)
#         print('Instanciate MQTT_Server')  
        
#         def on_connect(client, userdata, flags, rc):
#             print("Connected with result code "+str(rc))

#             client.subscribe(self.topic_sub1)
#             client.subscribe(self.topic_sub2)

#         # The callback for when a PUBLISH message is received from the server.
#         def on_message(client, userdata, msg):

#             # print('------------------------------Light intensity------------------------------')
#             # print(msg.topic+": "+str(msg.payload.decode("utf-8")))
#             # self.lightIntensity = int(msg.payload.decode("utf-8"))
#             # self.data = int(msg.payload.decode("utf-8"))
#             if(msg.topic == self.topic_sub1):
#                 self.lightIntensity = int(msg.payload.decode("utf-8"))
#                 # print(self.lightIntensity)
#             if(msg.topic == self.topic_sub2):
#                 self.rfid = int(msg.payload.decode("utf-8"))
#                 # print(self.rfid)

#         client = mqtt.Client()
#         client.on_connect = on_connect
#         client.on_message = on_message

#         client.connect(self.broker_address, 1883, 60)
#         client.loop_start()
#         # client.loop_forever()


#     def getLightIntensity(self):
#         # print('------------------------------Light intensity------------------------------')
#         print(self.lightIntensity)
#         return self.lightIntensity
        
#     def getRfid(self):
#         user_info = self.user_model.select_user(self.rfid)
#         print(f'user info {user_info}')
#         user = None
#         if(user_info):
#             user = {
#                 'user_id' : user_info[0],
#                 'user_name' : user_info[1],
#                 'user_email' : user_info[2],
#                 'temp_threshold' : user_info[3],
#                 'hum_threshold' : user_info[4],
#                 'intensity_threshold' : user_info[5],
#             }
#         # print(user)
#         return user
#         # print(f'RFID Tag: {self.rfid}')
#         # return self.rfid

    
# if __name__ == "__main__":
#     topic = IoTController()
#     print(topic.getLightIntensity())
#     print(topic.getRfid())


# -------------------------------------------
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
        print(f'============> Intensity: {self.lightIntensity}')
        return self.lightIntensity
        
    def getRfid(self):
        
        user_info = self.user_model.select_user(self.rfid)
        # print(self.rfid) 
        print(f'============> User Info: {user_info}')
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

# Example usage:
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
