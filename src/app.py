from  utils import *
import constants as CONS

import adafruit_helper as ada
import mask_detection as mdect

import yolobit_controller as yolobit
import firebase_services as firebase
from datetime import datetime
import base64
import uuid
import time
import threading
import cv2
import json

TaskQueue = []
# *********************** Yolobit Process *******************************
def yolobit_on_subscribe(feed_id, payload):

    if CONS.Feeds.Feed1.value in feed_id:
        yolobit.setAlarm(parse_value(payload, int))
        return True

    if  CONS.Feeds.Feed2.value in feed_id:
        yolobit.setFan(parse_value(payload, int))
        return True 

    if  CONS.Feeds.Feed3.value in feed_id:
        yolobit.setLed(parse_value(payload, int))
        return True
    
    if CONS.Feeds.Feed8.value in feed_id: 
        CONS.IsRunFaceDetection = parse_value(payload, int) == 1
        if CONS.IsRunFaceDetection:
            CONS.IsRunFaceDetection = False
            time.sleep(2)
            Task4_Run()     
        return True
        
    return False

def yolobit_on_env_sync(temperature, humidity):
    if len(str(temperature)) > 0:
        print(temperature)
        ada.publish(ada.mqtt_client, CONS.Feeds.Feed6.value, str(temperature))

    if len(str(humidity)) > 0:
        print(humidity)
        ada.publish(ada.mqtt_client, CONS.Feeds.Feed5.value, str(humidity))
    
# *********************** Mask Detection Process *******************************
def on_detection(_image, imgbase64, state, is_stranger = False):
    img_str = ""
    try:
        img_str = base64.b64encode(_image)
        if CONS.Detection_Counter % 3 == 0:
            print(">>>>>  On Mask Detection: " + state)

            ada.publish(ada.mqtt_client, CONS.Feeds.Feed4.value, imgbase64)
            ada.publish(ada.mqtt_client, CONS.Feeds.Feed7.value, state)

    except Exception as e: print(e)

    try:   
        if is_stranger:
            print("\n>> Detect Stranger")
            _id = str(uuid.uuid4()).replace("-","")
            _data = { "id": _id, "image": img_str.decode('utf-8'), "name": "Unknow", "state": state , "date": datetime.now().isoformat()}
            CONS.Detection_Counter = CONS.Detection_Counter + 1

            firebase.add_face(_id, _data)


            cv2.imwrite('./images/' + _id + '.jpg', _image)
            CONS.IsFaceDataSetUpdated = True    

    except Exception as e: print(e)

    try:
        if CONS.Detection_Counter == 5:
            yolobit.setAlarm(1)
            yolobit.setLed(1)
            CONS.Detection_Counter = 0
    except Exception as e: print(e)



# *********************** Tasks *******************************
def Task1_Run():
    def on_submit(key, value):
            print(">>>>>  Update Object Name: " + value)
            ada.publish(ada.mqtt_client, CONS.Feeds.Feed9.value, str(value))

    firebase.init(on_submit)


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

    Task1_Run() # Firebase
    Task2_Run() # AdFRUIT io MQTT 
    # Task3_Run() #Yolobit
    Task4_Run() # Face detection
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
        
    

