# Obj : The main class that initializes paho_mqtt Client objec.
# And calls the on_connect and on_message functors.
# Read more here : eclipse.org/paho/index.php?page=clients/python/docs/index.php

from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish

# Subscribe to some topic : topic
def on_connect(client , userdata, flags, rc):
    print(f"Connected to broker and the server return code : {rc}")

# Got a message from MQTT server : release to its callback
def on_message(client, userdata, msg):
    subbed_topics = client.comm_config.get("subscribed_topics")
    print(subbed_topics)
    assert(isinstance(subbed_topics, list))
    # Call the functor attached to msg.topic
    functor = client.comm_config.get("subscribed_topics")[msg.topic]
    return functor(msg.payload)


class Communicator:
    def __init__(self, comm_config):
        self.client = mqtt.Client()
        self.client.on_connect =  on_connect
        self.client.on_message = on_message
        self.comm_config = comm_config
        for topic in self.comm_config["subscribed_topics"]:
            print(topic)
            self.client.subscribe(topic)
    
    def run_mqtt_client(self):
        print(self.comm_config["broker"])
        self.client.connect(
            host = self.comm_config["broker"].get("ip"), 
            port = self.comm_config["broker"].get("port")
        )
        sleep(10)
        print("Starting Loop!")
        self.client.loop_start()
        print("Stopping Loop!")
    
    def stop_mqtt_client(self):
        self.client.loop_stop()
    
    def send_message_to_broker(self, topic, payload):
        print(self.comm_config.get("broker").get("ip"), self.comm_config.get("broker").get("port"))
        mqtt_publish.single(
            topic = topic,
            payload = payload, 
            qos = 0, 
            hostname = self.comm_config.get("broker").get("ip"),
            port = self.comm_config.get("broker").get("port")
        )