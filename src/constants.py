# Web	https://io.adafruit.com/khanhpnp/feeds/bg1
# API	https://io.adafruit.com/api/v2/khanhpnp/feeds/bg1
# MQTT
# by Key	khanhpnp/feeds/bg1
from enum import Enum

IsQuit = False
IsRunFaceDetection = True
Detection_Counter = 0
IsFaceDataSetUpdated = False

FaceDataSet = {}

class Feeds(Enum):
    Feed1 = "alarm-state"
    Feed2 = "fan-state"
    Feed3 = "led-state"
    Feed4 = "image"
    Feed5 = "humidity-meter"
    Feed6 = "temperature-meter"
    Feed7 = "message"

    Feed8 = "shutdown"
    Feed9 = "logs"
    Feed10 = "Feed10"
