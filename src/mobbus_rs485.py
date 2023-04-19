from iot_device import *
import serial.tools.list_ports

#class MobbusRs485:
device = None
RELAY1_ON = [0, 6, 0, 0, 0, 255, 200, 91]
RELAY1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

# Extend for the second Actuator
RELAY2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
RELAY2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

# Read Soil Temperature
SOIL_TEMPERATURE = [1, 3, 0, 6, 0, 1, 100, 11]
# Read Soil Moisture
SOIL_MOISTURE = [1, 3, 0, 7, 0, 1, 53, 203]

on_submit = None

def Run(_on_submit):
    global device
    global on_submit

    # create a new IoTDevice object
    device = IoTDevice(port='COM5', baudrate=9600, timeout=1)

    # connect to the device
    device.connect()

    # send a command to the device
    device.send_command('Hello!')

    # device.onListener = readData
    # # start listening for incoming data
    # device.start_listening()

    on_submit = _on_submit


# Send command to Actuators
def setRelayState(state, deviceId="1"):
    print("setDevice1 => State: " + str(state))

    if (deviceId == "1"):
        relayCommand = RELAY1_ON if state == True else RELAY1_OFF
        device.write(relayCommand)
    else:
        relayCommand = RELAY2_ON if state == True else RELAY2_OFF
        device.write(relayCommand)

    return state

# Receive Response
def readCommand():
    bytesToRead = device.inWaiting()
    if bytesToRead > 0:
        out = device.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * \
                256 + data_array[array_size-3]
            return value
        else:
            return -1

    return 0
