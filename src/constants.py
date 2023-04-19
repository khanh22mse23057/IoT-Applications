# Web	https://io.adafruit.com/khanhpnp/feeds/bg1
# API	https://io.adafruit.com/api/v2/khanhpnp/feeds/bg1
# MQTT
# by Key	khanhpnp/feeds/bg1
from enum import Enum

IsQuit = False
IsRunFaceDetection = True

class Feeds(Enum):
    Feed1 = "alarm_state"
    Feed2 = "fan_state"
    Feed3 = "led_state"
    Feed4 = "image"
    Feed5 = "humidity_meter"
    Feed6 = "temperature_meter"
    Feed7 = "message"

    Feed8 = "shutdown"
    Feed9 = "Feed9"
    Feed10 = "Feed10"
