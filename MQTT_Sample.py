# pip install paho-mqtt
import paho.mqtt.client as mqtt
import json

# topic_sub = "IoTlab/ESP"
topic_sub = "ESP8266/Photoresister" 
# topic_sub = "ESP8266/Sensor" 

# broker_address = "mqtt.eclipseprojects.io"
broker_address = "192.168.0.157"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_sub)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # msg_json = json.load(msg.payload.decode())
    # print(msg.payload.decode())
    # print(msg.topic+": "+str(msg.payload))

    print(msg.topic+": "+str(msg.payload.decode("utf-8")))


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
    # client.loop_start()


if __name__ == '__main__':
    main()