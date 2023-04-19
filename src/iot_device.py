import serial
import threading
import time
from  constants import *
class IoTDevice:

    on_listener = None
    cmd_buffer = ""

    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.thread = None
        self.on_listener = None

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

        if self.serial != None:
            print("Connected to {0} {1}".format(self.port, self.baudrate))

    def disconnect(self):
        if self.serial:
            self.serial.close()

        if self.thread:
            self.thread.join()

    def send_command(self, command):
        print("Sending command: " + str(command))
        if self.serial:
            self.serial.write(str(command).encode())

    def handle_data(self, data):
        # do something with the data
        print("Received data:", data)

    def read_command(self):
        bytesToRead = self.serial.inWaiting()
 
        if (bytesToRead > 0):
            nData = self.serial.read(bytesToRead).decode("UTF-8")
            self.cmd_buffer = self.cmd_buffer + nData
            print("\n" + nData)
            while ("#" in self.cmd_buffer) and ("!" in self.cmd_buffer):
                return nData

    def listen(self):
        print(">>> Start IoTDevice Listner")
        while True:
            if IsRunFaceDetection == False:
                self.disconnect()
                return
            # data = self.serial.readline().decode().strip()
            data = self.read_command()
            if data:
                print(data)
                self.on_listener(str(data))

            time.sleep(1)

    def start_listening(self):
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    # Get serial com port
    def getPort(self):
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