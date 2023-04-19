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
from datetime import datetime

TaskQueue = []
# *********************** Yolobit Process *******************************
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
        CONS.IsRunFaceDetection = parse_value(payload, int) == 1
        if CONS.IsRunFaceDetection:
            CONS.IsRunFaceDetection = False
            time.sleep(2)
            Task4_Run()     
        return True
    
    
    return False

def yolobit_on_env_sync(temperature, humidity):
    if len(temperature) > 0:
        print(temperature)
        ada.publish(ada.mqtt_client, CONS.Feeds.Feed5.value, temperature)

    if len(humidity) > 0:
        print(temperature)
        ada.publish(ada.mqtt_client, CONS.Feeds.Feed6.value, humidity)
    
# *********************** Mask Detection Process *******************************

def on_detection(_image, imgbase64, state):
    try:
        print(">>>>>  On Mask Detection: " + state)
        img_str = base64.b64encode(_image)
        ada.mqtt_client.publish(CONS.Feeds.Feed4.value, imgbase64)
        ada.mqtt_client.publish(CONS.Feeds.Feed7.value, state)
    except Exception as e: print(e)

    try:   
        
        data = { "id": str(uuid.uuid4()), "image": img_str.decode('utf-8'), "state": state , "date": datetime.now().isoformat()}
        firebase.writePost(data["id"], data)
    
    except Exception as e: print(e)


# *********************** Tasks *******************************
def Task1_Run():
    firebase.init()

def Task2_Run():
    try:
        ada.onRecivedData = yolobit_on_subscribe
        ada.ping()
    except Exception as e: print(e)

def Task3_Run():
    try:
        yolobit.Run(yolobit_on_env_sync)

    except Exception as e: print(e)
    

def Task4_Run():
    print(">> Detecting the human face") 
    CONS.IsRunFaceDetection = True
    def run_detection():
        try:
            mdect.run_detection(on_detection)
        except Exception as e: 
            print(e)

    t2 = threading.Thread(target=run_detection, args=())
    t2.start()

    TaskQueue.append(t2)


# *********************** App Run *******************************
def run():

    Task1_Run()
    Task2_Run()
    Task3_Run()
    # Task4_Run()

    while True:

        time.sleep(0.01)
        command = input()
        if command.lower() == "quit":
            CONS.IsQuit = True
            print("Goodbye!")
            yolobit.disconnect()
            break


    for task in TaskQueue:
        try:
            print(">> Release Task")
            task.join() 
        except: print("Error !")
        
    

