import adafruit_helper as ada
import mask_detection as mdect
import face_recognitions as frecog
import base64
import constants as CONS
import yolobit_controller as yolobit
import firebase_services as firebase
import uuid
import time
import threading
from  utils import *

def onUnMaskDetection(_image, imgbase64, state):
    try:
        print(">>>>>  onUnMaskDetection: " + state)
        img_str = base64.b64encode(_image)
        ada.mqtt_client.publish(CONS.Feeds.Feed4.value, imgbase64)
        ada.mqtt_client.publish(CONS.Feeds.Feed7.value, state)
    except Exception as e: print(e)

    try:
    
        
        data = { "id": str(uuid.uuid4()), "image": img_str.decode('utf-8'), "state": state }
        firebase.writePost(data["id"], data)
    
    except Exception as e: print(e)


def yolobit_on_subscribe(feed_id, payload):

    if feed_id == CONS.Feeds.Feed1.value:
        yolobit.setAlarm(parse_value(payload, int))
        return True

    if feed_id == CONS.Feeds.Feed2.value:
        yolobit.setFan(parse_value(payload, int))
        return True 

    if feed_id == CONS.Feeds.Feed3.value:
        yolobit.setLed(parse_value(payload, int))
        return True
    
    if feed_id == CONS.Feeds.Feed8.value:        
        CONS.IsQuit = parse_value(payload, int) == 1
        return True
    
    return False

def yolobit_on_env_sync(temperature, humidity):
    if len(temperature) > 0:
        print(temperature)
        ada.publish(CONS.Feeds.Feed5.value, temperature)

    if len(humidity) > 0:
        print(temperature)
        ada.publish(CONS.Feeds.Feed6.value, humidity)
    
    
def run_detection():
    mdect.run_detection(onUnMaskDetection)

def run():
    ada.onRecivedData = yolobit_on_subscribe
    ada.ping()

    t1 = threading.Thread(target=run_detection, args=())
    t1.start()
    #frecog.run_face_recognition()
    #yolobit.__init__()
    firebase.init()
    while True:
        #yolobit.onDataFlow(yolobit_on_env_sync)
        command = input()
        if command.lower() == "quit":
            CONS.IsQuit = True
            print("Goodbye!")
            break

    t1.join()
    

