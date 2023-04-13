# Set to your Adafruit IO key.

# Remember, your key is a secret so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_TqMv96AVHGXcQT30SC4rNSayzted'

# Set to your Adafruit IO username. (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'khanhpnp90'

# IO Feed Owner's username
IO_FEED_USERNAME = 'khanhpnp'

# Make sure you have read AND write access to this feed to publish.
IO_FEED = 'logs'

import time
def getStart():
# get the start time
    return time.process_time()

def getProcessTime(st):
# get the start time
    return time.process_time() - st