import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def scan_rfid(reader=SimpleMFRC522()):
    """
    Using SimpleMFRC522, read input from Raspberry Pi.
    https://github.com/pimylifeup/MFRC522-python
    """
    try:
        id = reader.read()[0]
        print('Read ID:', id)
    except: # ToDo - not sure what exceptions could be thrown
        print('Error reading RFID card')
        raise
    return id


if __name__ == '__main__':
    reader = SimpleMFRC522()
    try:
        while True:
            scan_rfid(reader)
            time.sleep(1)
    
    # Stop on Ctrl+C and clean up
    except KeyboardInterrupt:
        GPIO.cleanup()
