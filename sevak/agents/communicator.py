# Obj : The main class that initializes paho_mqtt Client objec.
# And calls the on_connect and on_message functors.
# Read more here : eclipse.org/paho/index.php?page=clients/python/docs/index.php

from time import sleep

import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish

# Subscribe to some topic : topic
def on_connect(client , userdata, flags, rc):
    print(f"Connected to broker and the broker returned code : {rc}")
    # Sub to topics now
    print(f"Subbed to topics : {' and '.join(userdata['subscribed_topics'])}")
    for topic in userdata["subscribed_topics"]:
        client.subscribe(topic)

# Got a message from MQTT server : release to its callback
def on_message(client, userdata : dict, msg : bytearray):
    assert isinstance(userdata, dict)
    subbed_topics = userdata.get("subscribed_topics")
    assert(isinstance(subbed_topics, list))
    # Call the functor attached to msg.topic
    functor = userdata.get("topic_functor_map")[msg.topic]
    # Convert bytearray to dict
    #payload = json.loads(msg.payload.decode("utf-8").replace("'",'"'))
    return functor(msg.payload)


class Communicator:
    def __init__(self, comm_config):
        self.comm_config = comm_config
        self.client = mqtt.Client(
            userdata = comm_config
            )
        self.client.on_connect =  on_connect
        self.client.on_message = on_message
        
    
    def run_mqtt_client(self):
        self.client.connect(
            host = self.comm_config["broker"].get("ip"), 
            port = self.comm_config["broker"].get("port")
        )
        # Wait for 1 seconds for connection
        sleep(1)
        self.client.loop_forever()
    
    def stop_mqtt_client(self):
        self.client.loop_stop()
    
    def send_message_to_broker(self, topic, payload):
        print(f"Publishing to topic : {topic}")
        mqtt_publish.single(
            topic = topic,
            payload = payload, 
            qos = 0, 
            hostname = self.comm_config.get("broker").get("ip"),
            port = self.comm_config.get("broker").get("port")
        )