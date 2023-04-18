# Import Adafruit IO MQTT client.
import sys
import constants as Cons
import config
from Adafruit_IO import MQTTClient

# Create an MQTT client instance.
mqtt_client  = MQTTClient(config.ADAFRUIT_IO_USERNAME, config.ADAFRUIT_IO_KEY)
onRecivedData = None
# Define callback functions which will be called when certain events happen.
def connected(client):
# Connected function will be called when the client connects.
    for feed in (Cons.Feeds):
        print('Subscribed feed: [{0}] .'.format(feed.value))  
        client.subscribe(feed.value)
    
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    onRecivedData(feed_id, payload)


def publish(client, feed_id, value):
    print('Publishing value: [{0}] to [{1}].'.format(value, feed_id))  
    client.publish(feed_id, value, config.ADAFRUIT_IO_USERNAME)

def ping():
    
    #mqtt_client = MQTTClient(config.ADAFRUIT_IO_USERNAME, config.ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    mqtt_client.on_connect = connected
    mqtt_client.on_disconnect = disconnected
    mqtt_client.on_message = message

    # Connect to the Adafruit IO server.
    mqtt_client.connect()
    mqtt_client.loop_background()
    print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')

    return mqtt_client
    


