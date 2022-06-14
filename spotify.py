#!/usr/bin/env python
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def validate_auth(client_id, client_secret):
    # Check if .cache path exists
    if not os.path.exists('.cache'):
        print('abort: Need to authenticate')
        # ToDo - publish message to AWS SNS topic
        sys.exit()
    
    # Spotify authentication
    try:
        auth_manager=SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri="http://localhost:8080",
                                scope="user-read-playback-state,user-modify-playback-state")
    except spotipy.oauth2.SpotifyOauthError:
        print('abort: Client ID and Client Secret not recognized')
        sys.exit()
        # ToDo - publish message to AWS SNS topic

    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_device_id(sp, device_name):
    devices = sp.devices()['devices']
    for d in devices:
        if d['name'] == device_name:
            return d['id']
    raise KeyError("Expected device name not present in user's Spotify connected devices")


def play(sp, device_id, uri, playback_type):
    """
    Reference: https://talaexe.com/moderndayrecordplayer
    """
    # Specify device for playback
    try:
        sp.transfer_playback(device_id=device_id, force_play=False)
    except spotipy.exceptions.SpotifyException as err:
        print(f'Issue transfering playback to device: {err}')

    # Play specific URI
    try:
        if playback_type == 'track':
            sp.start_playback(device_id=device_id, uris=[f'spotify:track:{uri}'])
        else:
            sp.start_playback(device_id=device_id, context_uri=f'spotify:{playback_type}:{uri}')
    except spotipy.exceptions.SpotifyException as err:
        print(f'Issue playing song: {err}')

if __name__ == '__main__':
    
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    DEVICE_ID = os.environ.get('DEVICE_ID')

    sp = validate_auth(CLIENT_ID, CLIENT_SECRET)
    play(sp=sp, device_id=DEVICE_ID, uri='09ulWjNT2O3rlYJCDZESBW', playback_type='track')
    # play(uri='37i9dQZF1DWVFzWmxRnRJH', playback_type='playlist')
    # play(uri='08XFx1OZMZnRCh0JrKTIgT', playback_type='album')
    
