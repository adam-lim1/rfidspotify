import argparse
import csv
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

def create_uri_lookup(file_name):
    """
    Convert CSV of format rfid, uri, asset_type to dictionary
    of format {rfid: {'uri': uri, 'asset_type': asset_type}}
    """
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        uri_lookup = {}
        for row in reader:
            rfid_key, uri, asset_type = [x.strip() for x in row]
            uri_lookup[rfid_key] = {'uri': uri, 'asset_type': asset_type}
    return uri_lookup
        

if __name__ == '__main__':
    
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    URI_FILE = os.environ.get('URI_FILE')

    uri_lookup = create_uri_lookup(URI_FILE)
    
    # Initialize Spotify
    device_name = parse_device_name()    
    sp = validate_auth(CLIENT_ID, CLIENT_SECRET) # ToDo - error handling
    device_id = get_device_id(sp, device_name)

    # Infinite loop for reading RFID input
    reader = SimpleMFRC522()
    try:
        while True:
            id = str(scan_rfid(reader))
            play(sp=sp, device_id=device_id, uri=uri_lookup[id]['uri'], playback_type=uri_lookup[id]['asset_type'])
            time.sleep(1)
    
    # Stop on Ctrl+C and clean up
    except KeyboardInterrupt:
        GPIO.cleanup()
    