from iot_device import *


device = None
buffer = ""
counter  = 0
onProcessData = None
QueueData = {}

def __init__():
    # create a new IoTDevice object
    device = IoTDevice(port='COM4', baudrate=9600, timeout=1)

    # connect to the device
    device.connect()

    # send a command to the device
    device.send_command('Hello!')

    device.onListener = readData

    # start listening for incoming data
    device.start_listening()

def setLed(state):
    print(state)

def setFan(state):
    print(state)   

def setAlarm(state):
    print(state)   

def getEnvironmentalData(command):
    command = command.replace("!", "")
    command = command.replace("#", "")
    data = command.split(":")

    temperature = data[2] if data[1] == "T" else ""
    humidity    = data[2] if data[1] == "H" else ""

    if len(temperature) > 0:
        QueueData["temperature"] = temperature.strip()
    if len(humidity) > 0:
        QueueData["humidity"] = humidity.strip()


def readData(message = None):

    while ("#" in message) and ("!" in message):
        start = message.find("!")
        end = message.find("#")
        data =  message[start:end + 1]
        message = (message[end+1:], "")[end == len(message)]
        
        processData(message)

        return message, data
    
def processData(data):
    getEnvironmentalData(data)

def onDataFlow(on_submit):
    time.sleep(0.1)
    global counter
    counter = counter + 1

    if counter == 50:

        temperature = QueueData["temperature"]
        humidity  = QueueData["humidity"]
        print(">>> Temperature: {} Humidity: {}".format(temperature, humidity))
            
        on_submit(temperature, humidity)
        counter = 0



