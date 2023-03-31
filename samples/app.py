import time
import random
import constants as Cons
import config
from adafruit_helper import *

#************************************************************************************************************************
def publish(count, max_count=5):
    
    _feed_id = Cons.Feeds.Feed1.value
    _count = (0 if count >= max_count else count + 1)

    if _count > 0:
        _feed_id = Cons.Feeds.Feed2.value
    
    mqtt_client.publish(_feed_id, _value:=random.randint(0, 100), config.ADAFRUIT_IO_USERNAME)

    return _count, _feed_id, _value

def sample1_publishing():    
    _count = 0
    while True:
        _count, _feed_id, _value = publish(_count)
        print('Publishing value: [{0}] to [{1}].'.format(_value, _feed_id))    
        time.sleep(1)


#************************************************************************************************************************
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(Cons.Feeds.Feed1.value)
    client.on_message = on_message

def sample2_subscribing():    
    _count = 0
    while True: 
        subscribe(mqtt_client)

#************************************************************************************************************************
def run():
    
    #sample1_publishing()
    sample2_subscribing()
