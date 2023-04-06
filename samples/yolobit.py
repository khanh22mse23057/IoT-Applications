import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient
import config


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

ser = serial.Serial( port=getPort(), baudrate=115200)

mess = ""

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish("bbc-temp", splitData[2])

mess = ""

def readSerial(client, count =1):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            #processData(mess[start:end + 1])

            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def push_data(client, temp, hum):
    client.publish("classroom_humidity", temp)
    client.publish("classroom_temperature", hum)

def yolobit_run(client):
    count = 1
    while True:
        readSerial(client, count)
        time.sleep(1)