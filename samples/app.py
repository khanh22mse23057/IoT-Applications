
from mask_detection import *
from yolobit import *
from modbus_rs485 import *
from mqtt_service import *
from face_recognitions import *
def run():    
    #sample1_publishing()
    #sample2_subscribing(mqtt_client)
    ping()
    #run_detection(mqtt_client)
    #ping()
    #yolobit_run(mqtt_client)
    #adafruit_run()
    #mobbus_run(mqtt_client)
    run_face_recognition(mqtt_client)
