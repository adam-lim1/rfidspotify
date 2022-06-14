import argparse
import os
import time

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

from rfid import scan_rfid
from spotify import validate_auth, get_device_id, play

def parse_device_name():
    """
    Parse command line input for --device or -d specifying name of 
    Spotify Connect device. If no input provided, fall back to sourcing
    desired device name from environment variable
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", help="Name of Spotify device to play on")
    args = parser.parse_args()

    if args.device:
        device_name = args.device
    else: # Source it from config
        device_name = os.environ.get('DEVICE_NAME')
    
    return device_name

if __name__ == '__main__':
    
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    
    # Initialize Spotify
    device_name = parse_device_name()    
    sp = validate_auth(CLIENT_ID, CLIENT_SECRET) # ToDo - error handling
    device_id = get_device_id(sp, device_name)

    # Infinite loop for reading RFID input
    reader = SimpleMFRC522()
    try:
        while True:
            id = scan_rfid(reader)
            # ToDo - Translate id to URI
            play(sp=sp, device_id=device_id, uri='09ulWjNT2O3rlYJCDZESBW', playback_type='track')
            time.sleep(1)
    
    # Stop on Ctrl+C and clean up
    except KeyboardInterrupt:
        GPIO.cleanup()
