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
def onUnMaskDetection(image, state):
    print(">>>>>  onUnMaskDetection: " + state)
    img_str = base64.b64encode(image)
    ada.mqtt_client.publish(CONS.Feeds.Feed4.value, img_str)
    ada.mqtt_client.publish(CONS.Feeds.Feed7.value, state)
    firebase.writePost(uuid.uuid4(), { "image": image, "state": state }),

def yolobit_on_subscribe(feed_id, payload):

    if feed_id == CONS.Feeds.Feed1.value:
        yolobit.setAlarm(int(payload))
        return True

    if feed_id == CONS.Feeds.Feed2.value:
        yolobit.setFan(int(payload))
        return True 

    if feed_id == CONS.Feeds.Feed3.value:
        yolobit.setLed(int(payload))
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
    ada.ping()
    # t1 = threading.Thread(target=run_detection, args=())
    # t1.start()
    #frecog.run_face_recognition()
    #yolobit.__init__()
    firebase.init()
    while True:
        # TODO: Add implementation
        #yolobit.onDataFlow(yolobit_on_env_sync)
        firebase.writePost(uuid.uuid4(), { "image": "image", "state": "state" })
        time.sleep(10)
        command = input()
        if command.lower() == "quit":
            print("Goodbye!")
            break


    # t1.join()
    

