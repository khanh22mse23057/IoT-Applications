import time
import serial.tools.list_ports
import threading

# Get serial com port
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


relay1_ON = [0,6,0,0,0,255,200,91]
relay1_OFF = [0,6,0,0,0,0,136,27]

relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

# Send command to Actuators
def setDevice1(ser, state):
    if state == True:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)

# Extend for the second Actuator
relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]


def setDevice2(ser, state):
    if state == True:
        ser.write(relay2_ON)
    else:
        ser.write(relay2_OFF)


# Receive Response
def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size-3]
            return value
        else:
            return -1
    return 0

# Read Soil Temperature
soil_temperature = [1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature(ser):
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

# Read Soil Moisture
soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture(ser):
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

def data_pushing(count):
    setDevice1(count % 2 == 0)
    setDevice2(count % 2 != 0)
    time.sleep(10)

def start():
    count = count + 1
    t = threading.Thread(target=data_pushing, args=(count))
    t.start()

count = 0
def mobbus_run():
    print("****** Sensor and Actuators")

    port = getPort()
    if port != "None":
        print("****** Port found" + port)
        serCom = serial.Serial(port=port, bauddrate=9600)
        while True:
            start()
    else:
        print("****** Port not found" + port)