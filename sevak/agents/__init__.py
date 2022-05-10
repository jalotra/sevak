
# How does comm_config look like ? 
'''
comm_config = {
    "subscribed_topics" : [subbed_topic_one, subbed_topic_two ...], 
    "topic_functor_map" : {
        "subbed_topic_one" : func_one, 
        "subbed_topic_two" : func_two
    }
    "broker" : {
        "ip" : some_IPV4_address_here, 
        "port" : some port >= 10000 here
    }
}
'''

# What are the MQTT topics ? 
# 1. get_image -> data/get_image/rgb_image
# 2. get_stream => data/get_stream/rgb_image
# 3. object_detection => ops/object_detection
# 4. maybe classification => ops/classification
# 5. more to come now.

from collections import OrderedDict
from configparser import ConfigParser

class CreateConfig:
    def __init__(self):
        self.comm_config = {
            "subscribed_topics" : [],
            "topic_functor_map" : dict(),
            "broker" : dict()
        }
        # Read broker details from config file in /configs/config.ini
        from configs.config import get_config_file_path
        with open(get_config_file_path(), "r") as f:
            config = ConfigParser()
            config.read_file(f)
        assert config.has_section("broker")
        self.add_broker_details(config.get("broker", "ip"), int(config.get("broker", "port")))


    def add_topic_and_functor(self, topic_name : str, topic_functor):
        assert topic_name is not None and topic_functor is not None
        self.comm_config["subscribed_topics"].append(topic_name)
        self.comm_config["topic_functor_map"][topic_name] = topic_functor
    
    def add_broker_details(self, ip : str, port : int):
        self.comm_config["broker"]["ip"] = ip
        self.comm_config["broker"]["port"] = port
    
    def get_comm_config(self):
        return self.comm_config


