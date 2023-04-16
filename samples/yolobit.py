import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient
import config
import threading
import constants as Cons
mess = ""


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM6"

def data_pushing(client, feed_id, value):
    time.sleep(10)
    client.publish(feed_id, value)
    print('Publishing value: [{0}] to [{1}].'.format(value, feed_id))  
    return

def processData(client, data):
    try:
            data = data.replace("!", "")
            data = data.replace("#", "")
            #splitData = data.split(":")
            print("Pushing data" + data)
            client.publish(Cons.Feeds.Feed8.value, data)
    except:
        print("An exception occurred")
    

    

    # feed_id = ("classroom_humidity" if splitData[1] == "H" else "classroom_temperature")
    # t = threading.Thread(target=data_pushing, args=(client,feed_id,splitData[2]))
    # t.start()


def writeData(com_ser, data):
    print(data)
    com_ser.write(str(data).encode())
   
def readSerial(com_ser, client, count =1):
    bytesToRead = com_ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + com_ser.read(bytesToRead).decode("UTF-8")
        print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            mess = (mess[end+1:], "")[end == len(mess)]

def push_data(client, temp, hum):
    client.publish("classroom_humidity", temp)
    client.publish("classroom_temperature", hum)

def connect_device():
    return serial.Serial( port=getPort(), baudrate=115200)
     
def subscribe(com_ser, client, feed_id):
    def on_message(client, feed_id, payload):
        print(f"Received `{payload}` from `{feed_id}` topic")

        if feed_id == Cons.Feeds.Feed2.value:
            if payload == "1":
                writeData(com_ser, 1)
            else:
                writeData(com_ser, 2)
            return

        # if feed_id == Cons.Feeds.Feed3.value:
        #     if payload == "1":
        #         writeData(com_ser, 3)
        #     else:
        #         writeData(com_ser, 4)  
        #     return      

    client.subscribe(feed_id)
    client.on_message = on_message

def yolobit_run(client):
    count = 1
    com_ser = connect_device()
    
    while True:
        readSerial(com_ser, client, count)
        # subscribe(com_ser, client, Cons.Feeds.Feed3)
        subscribe(com_ser , client, Cons.Feeds.Feed8)
        time.sleep(1)