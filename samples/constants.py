# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = ''
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'khanhpnp'
# Shared IO Feed
# IO Feed Owner's username
IO_FEED_USERNAME = 'khanhpnp'
# Make sure you have read AND write access to this feed to publish.
IO_FEED = 'SHARED_AIO_FEED_NAME'


# Web	https://io.adafruit.com/khanhpnp/feeds/bg1
# API	https://io.adafruit.com/api/v2/khanhpnp/feeds/bg1
# MQTT
# by Key	khanhpnp/feeds/bg1


from enum import Enum
class Feeds(Enum):
    Feed1 = 'mse11-sensor01'
    Feed2 = 'mse11-sensor02'
    Feed3 = 'mse11-sensor03'