import serial
import threading
import time
class IoTDevice:

    onListener = None
    command = ""

    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.thread = None
        self.onListener = None

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

        if self.serial != None:
            print("Connected to {} {}".format(self.port, self.baudrate))

    def disconnect(self):
        if self.serial:
            self.serial.close()
        if self.thread:
            self.thread.join()

    def send_command(self, command):
        if self.serial:
            self.serial.write(str(command).encode())

    def handle_data(self, data):
        # do something with the data
        print("Received data:", data)

    def read_command(self):
        bytesToRead = self.serial.inWaiting()
 
        if (bytesToRead > 0):
            global command
            
            command = command + self.serial.read(bytesToRead).decode("UTF-8")
            print(command)
            while ("#" in command) and ("!" in command):
                return command

    def listen(self):
        print(">>> Start IoTDevice Listner")
        while True:
            data = self.serial.readline().decode().strip()
            if data:
                print(data)
                self.onListener(data)

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