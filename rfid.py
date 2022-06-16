import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def scan_rfid(reader=SimpleMFRC522()):
    """
    Using SimpleMFRC522, read input from Raspberry Pi.
    Waits for RFID input to be provided.
    https://github.com/pimylifeup/MFRC522-python
    """
    try:
        id = reader.read()[0]
        print('Read ID:', id)
    except: # ToDo - not sure what exceptions could be thrown
        print('Error reading RFID card')
        raise
    return id

def scan_rfid_no_block(reader=SimpleMFRC522()):
    """
    Modification to SimpleMFRC522 read_id_no_block.
    Returns None if no RFID card provided.
    Attempts to read twice due to issue: https://github.com/pimylifeup/MFRC522-python/issues/15
    """
    def _wrapped_read_no_block(reader):
        try:
            id = reader.read_id_no_block()
        except:
            print('Error reading RFID')
            raise
        return id
    
    id = _wrapped_read_no_block(reader)
    if id is None:
        id = _wrapped_read_no_block(reader)
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
