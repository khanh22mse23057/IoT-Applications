from iot_device import IoTDevice
import time

device = None
buffer = ""
counter  = 0
QueueData = {
    "temperature" :"",
    "humidity": ""
}
on_submit = None

def Run(_on_submit):
    global device
    global on_submit
    # create a new IoTDevice object
    device = IoTDevice(port='COM7', baudrate=115200, timeout=1)

    # connect to the device
    device.connect()

    # send a command to the device
    device.send_command('Hello!')

    device.on_listener = readData

    # start listening for incoming data
    device.start_listening()


    on_submit = _on_submit

def setLed(state):

    cmd = 1 if state == 1 else 2    

    print("{0} => {1}".format(state,cmd ))
    global device
    device.send_command(cmd)

def setFan(state):

    cmd = 3 if state == 1 else 4    
    print("{0} => {1}".format(state,cmd))

    global device
    device.send_command(cmd)  

def setAlarm(state):
    cmd = 5 if state == 1 else 6  
    print("{0} => {1}".format(state,cmd ))

    device.send_command(cmd)   

def disconnect():
    device.disconnect()

def getEnvironmentalData(command):
    try:
        command = command.replace("!", "")
        command = command.replace("#", "")
        data = command.split(":")
        global QueueData
        if len(data) > 2:
            temperature = data[2] if data[1] == "T" else ""
            humidity    = data[2] if data[1] == "H" else ""
            if len(temperature) > 0:
                QueueData["temperature"] = temperature.strip()
            if len(humidity) > 0:
                QueueData["humidity"] = humidity.strip()

    except Exception as e: print(e)

def readData(message = None):
    print(">> Process cmd: " + message)
    while ("#" in message) and ("!" in message):
        start = message.find("!")
        end = message.find("#")
        data =  message[start:end + 1]
        message = (message[end+1:], "")[end == len(message)]
        
        processData(message)

        return message, data
    
def processData(data):
    getEnvironmentalData(data)
    onDataFlow()

def onDataFlow():
    global counter
    counter = counter + 1

    if counter == 100:
        global QueueData
        temperature = QueueData["temperature"]
        humidity  = QueueData["humidity"]
        print(">>> Temperature: {0} Humidity: {1}".format(temperature, humidity))
        counter = 0

        global on_submit
        on_submit(temperature, humidity)

    time.sleep(0.1)
    



