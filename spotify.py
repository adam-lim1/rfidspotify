#!/usr/bin/env python
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def validate_auth():
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    # Check if .cache path exists
    if not os.path.exists('.cache'):
        print('abort: Need to authenticate')
        # ToDo - publish message to AWS SNS topic
        sys.exit()
    else:
        # Spotify authentication
        auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri="http://localhost:8080",
                                scope="user-read-playback-state,user-modify-playback-state")
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp


def play(sp, uri, playback_type):
    """
    Reference: https://talaexe.com/moderndayrecordplayer
    """
    # Read from environment variables (source config.txt first)
    DEVICE_ID = os.environ.get('DEVICE_ID')

    # Specify device for playback
    try:
        sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

        # Play specific URI
        if playback_type == 'track':
            sp.start_playback(device_id=DEVICE_ID, uris=[f'spotify:track:{uri}'])
        else:
            sp.start_playback(device_id=DEVICE_ID, context_uri=f'spotify:{playback_type}:{uri}')
    
    except spotipy.exceptions.SpotifyException:
        print('Issue playing song')

if __name__ == '__main__':
    sp = validate_auth()
    play(sp=sp, uri='09ulWjNT2O3rlYJCDZESBW', playback_type='track')
    # play(uri='37i9dQZF1DWVFzWmxRnRJH', playback_type='playlist')
    # play(uri='08XFx1OZMZnRCh0JrKTIgT', playback_type='album')
    
