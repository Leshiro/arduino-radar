# imports
import serial.tools.list_ports

# autofind COM port
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(keyword in (port.description + port.manufacturer or '').lower() for keyword in ['arduino', 'ch340', 'cp210', 'ftdi', 'usb serial']):
            return port.device
    return None

# display settings
TITLE = "ARDUINO ULTRASONIC RADAR"
WINDOW_TITLE = f"Arduino Ultrasonic Radar"
W, H = 1000, 640

# settings
PORT = find_arduino_port() # usb port
BAUD = 9600

MAX_DIST = 50 # distance cap
MAX_TRAIL = 150 # fadeout delay

# initials
INITIAL_ANGLE = 90.0
INITIAL_DISTANCE = 0.0