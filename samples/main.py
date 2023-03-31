# Import standard python modules.
import sys
import time
import random
# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

import constants as Cons


# Define callback functions which will be called when certain events happen.
def connected(client):
# Connected function will be called when the client connects.
    client.subscribe(Cons.Feeds.Feed1, Cons.ADAFRUIT_IO_USERNAME)

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

# Create an MQTT client instance.
client = MQTTClient(Cons.ADAFRUIT_IO_USERNAME, Cons.ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message


# Connect to the Adafruit IO server.
client.connect()
client.loop_background()
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')


def publish_sample1(count, max_count=5):
    
    count = (0 if count >= max_count else count + 1)
    feed_id = Cons.Feeds.Feed1.value
    value = random.randint(0, 100)

    if count > 0:
        feed_id = Cons.Feeds.Feed2.value
    
    client.publish(feed_id, value, Cons.ADAFRUIT_IO_USERNAME)
    return count, feed_id, value

count = 0
while True:

    count, feed_id, value = publish_sample1(count)    
    print('Publishing value: [{0}] to [{1}].'.format(value, feed_id))    
    time.sleep(1)
