#!/usr/bin/env python
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authenticate(client_id, client_secret):
    """
    Authenticate w/ oauth2 protocol. 
    Requires user interaction to get redirect URL
    """

    try:
        auth_manager=SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri="http://localhost:8080",
                                scope="user-read-playback-state,user-modify-playback-state")
    except spotipy.oauth2.SpotifyOauthError:
        print('abort: Need to source config variables')
        sys.exit()
        # ToDo - publish message to AWS SNS topic

    sp = spotipy.Spotify(auth_manager=auth_manager)

    print(sp.me())
    return

if __name__ == '__main__':
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    authenticate(CLIENT_ID, CLIENT_SECRET)
