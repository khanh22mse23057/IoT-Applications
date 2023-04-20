import time
import os

# Set to your Adafruit IO key.
# Remember, your key is a secret so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_XGXU09cseCORTWjuQvy0CNnatkOa'
# Set to your Adafruit IO username. (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'khanhpnp90'
# IO Feed Owner's username
IO_FEED_USERNAME = 'khanhpnp90'

# Define the IP address and port of the camera
CAMERA_IP_ADDRESS = ""
CAMERA_IP_PORT = "4747"
# Set up the URL for the camera feed
CAMERA_IP_URL = f"http://{CAMERA_IP_ADDRESS}:{CAMERA_IP_PORT}/video"


import ipaddress

def is_valid_lan_ip(ip):
    try:
        # Create an IPv4Address object from the given IP address
        addr = ipaddress.IPv4Address(ip)
        
        # Check if the address is a private IP address
        return addr.is_private
    except ipaddress.AddressValueError:
        # The given IP address is not a valid IPv4 address
        return False
    
def checkIpCamera():
    # Ping the camera to check if it is ready
    #response = os.system("ping -c 1 " + CAMERA_IP_ADDRESS)

    if is_valid_lan_ip(CAMERA_IP_ADDRESS):
        print("Camera is ready. Connecting...")
        return True
        # Your code to connect to the camera goes here
    else:
        print("Could not connect to camera. Please check the IP address and try again.")
        return False

def getStart():
# get the start time
    return time.process_time()

def getProcessTime(st):
# get the start time
    return time.process_time() - st


