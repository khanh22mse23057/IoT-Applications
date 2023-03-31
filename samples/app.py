import time
import random
import constants as Cons
import config
from adafruit_helper import *


def publish_sample1(count, max_count=5):
    
    _feed_id = Cons.Feeds.Feed1.value
    _count = (0 if count >= max_count else count + 1)

    if _count > 0:
        _feed_id = Cons.Feeds.Feed2.value
    
    mqtt_client.publish(_feed_id, _value:=random.randint(0, 100), config.ADAFRUIT_IO_USERNAME)

    return _count, _feed_id, _value


def sample1(count=0):    
    _count, _feed_id, _value = publish_sample1(count)
    print('Publishing value: [{0}] to [{1}].'.format(_value, _feed_id))    
    time.sleep(1)

    return _count

def run():
    count = 0
    while True:
      count = sample1(count)
