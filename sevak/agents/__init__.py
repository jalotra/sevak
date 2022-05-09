
# How does comm_config look like ? 
'''
comm_config = {
    "topics" : [list of possible topics to subscribe to], 
    "subbed_topics" : {
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