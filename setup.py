#!/usr/bin/env python
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authenticate():
    """
    Authenticate w/ oauth2 protocol. 
    Requires user interaction to get redirect URL
    """
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri="http://localhost:8080",
                                scope="user-read-playback-state,user-modify-playback-state",
                                open_browser=False)

    sp = spotipy.Spotify(auth_manager=auth_manager)

    print(sp.me())
    return

if __name__ == '__main__':
    authenticate()
