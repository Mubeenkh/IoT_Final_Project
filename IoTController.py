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


class IoTController:
	
    topic_sub1 = "ESP8266/Photoresister"
    topic_sub2 = "ESP8266/RFID" 
    topic = ""
    # broker_address = "192.168.0.157"
    # broker_address = "172.20.10.2"    
    broker_address = "192.168.2.40"

    lightIntensity = 0
    rfid = 0

    lightIntensity = 0
    data = 0
    
    DB_FILE = 'user_data.db'
    user_model = None
    
    def __init__(self):
        print('Viewing User Model')
        self.user_model = IoTModel(self.DB_FILE)
        print('Instanciate MQTT_Server')  
        
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))

            client.subscribe(self.topic_sub1)
            client.subscribe(self.topic_sub2)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):

            # print('------------------------------Light intensity------------------------------')
            # print(msg.topic+": "+str(msg.payload.decode("utf-8")))
            # self.lightIntensity = int(msg.payload.decode("utf-8"))
            # self.data = int(msg.payload.decode("utf-8"))
            if(msg.topic == self.topic_sub1):
                self.lightIntensity = int(msg.payload.decode("utf-8"))
                # print(self.lightIntensity)
            if(msg.topic == self.topic_sub2):
                self.rfid = int(msg.payload.decode("utf-8"))
                # print(self.rfid)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(self.broker_address, 1883, 60)
        client.loop_start()
        # client.loop_forever()


    def getLightIntensity(self):
        # print('------------------------------Light intensity------------------------------')
        print(self.lightIntensity)
        return self.lightIntensity
        
    def getRfid(self):
        user_info = self.user_model.select_user(self.rfid)
        print(f'user info {user_info}')
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
        # print(f'RFID Tag: {self.rfid}')
        # return self.rfid

    
if __name__ == "__main__":
    topic = IoTController()
    print(topic.getLightIntensity())
    print(topic.getRfid())


# -------------------------------------------
# class IoTController:
	
#     topic_sub1 = "ESP8266/Photoresister"
#     topic_sub2 = "ESP8266/RFID" 
#     topic = ""
#     broker_address = "192.168.0.157"


#     lightIntensity = 0
#     rfid = 0
    
#     def __init__(self):
#         print('Instanciate MQTT_Server')

#     def connect(self):    
#         def on_connect(client, userdata, flags, rc):
#             print("Connected with result code "+str(rc))

#         client = mqtt.Client()
#         client.on_connect = on_connect
#         client.connect(self.broker_address, 1883, 60)
#         return client

#     def subscribe_topic(self, client, topic):   

#         # The callback for when a PUBLISH message is received from the server.
#         def on_message(client, userdata, msg):

#             # print('------------------------------Light intensity------------------------------')
#             # print(msg.topic+": "+str(msg.payload.decode("utf-8")))
#             # self.lightIntensity = int(msg.payload.decode("utf-8"))
#             # self.rfid = int(msg.payload.decode("utf-8"))
#             if(msg.topic == self.topic_sub1):
#                 self.lightIntensity = int(msg.payload.decode("utf-8"))
#             if(msg.topic == self.topic_sub2):
#                 self.rfid = int(msg.payload.decode("utf-8"))

#         client.subscribe(topic)
#         client.on_message = on_message
#         # client.loop_start()
#         # return self.data

#     def run(self, client):
#         # client.loop_forever()
#         client.loop_start()

#     def getLightIntensity(self):
#         print(f'Light Intensity: {self.lightIntensity}')
#         return self.lightIntensity
    
#     def getRfid(self):
#         print(f'RFID Tag: {self.rfid}')
#         return self.rfid
    
# if __name__ == "__main__":
#     topic = IoTController()
#     client = topic.connect() 
#     topic.subscribe_topic(client, "ESP8266/Photoresister")
#     topic.subscribe_topic(client, "ESP8266/RFID")
#     topic.run(client)
#     print(f"dsdsdsd {topic.getLightIntensity}")
#     print(f'opiopiio {topic.getRfid}')

# ------------------------------------------------
