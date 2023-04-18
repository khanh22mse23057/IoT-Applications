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

def __init__(self):
    # create a new IoTDevice object
    device = IoTDevice(port='COM5', baudrate=9600, timeout=1)

    # connect to the device
    device.connect()

    # send a command to the device
    device.send_command('Hello!')

    device.onListener = self.readData

    # start listening for incoming data
    device.start_listening()


# Send command to Actuators
def setRelayState(self, state, deviceId="1"):
    print("setDevice1 => State: " + str(state))

    if (deviceId == "1"):
        relayCommand = self.RELAY1_ON if state == True else self.RELAY1_OFF
        self.device.write(relayCommand)
    else:
        relayCommand = self.RELAY2_ON if state == True else self.RELAY2_OFF
        self.device.write(relayCommand)

    return state

# Receive Response
def readCommand(self):
    bytesToRead = self.device.inWaiting()
    if bytesToRead > 0:
        out = self.device.read(bytesToRead)
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
