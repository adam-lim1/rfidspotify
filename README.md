
# RFID Spotify Player

## Resources
- RFID Spotify Player: https://talaexe.com/moderndayrecordplayer
- Configuring Headless Raspberry Pi: https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html,  https://www.hackster.io/435738/how-to-setup-your-raspberry-pi-headless-8a905f
- Running program automatically at Raspberry Pi boot: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

## Setup

**Creating Virtual Environment**
```bash
pip install --upgrade pip
pip install --upgrade virtualenv
pip install --upgrade virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv rfidspotify
pip install requirements.txt
```

**Running RFID Spotify App**
```bash
ssh pi@raspberrypi.local
cd ~/Documents/rfidspotify/
source rfidspotify/bin/activate
source config.txt
python run.py [-d device]
```
- `-d` or `--device` is an optional flag that specifies which Spotify Connect device to start playback on. Default is `DEVICE_NAME` environment variable

**Configuring to Run Automatically at Raspberry Pi Startup**
```bash
cd ~
echo "cd /home/pi/Documents/rfidspotify" >> .bashrc
echo "sudo ./boot.sh" >> .bashrc
```

## Extra
**Get Spotify Album Art**
```python
import os
import requests
from spotify import validate_auth

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
sp = validate_auth(CLIENT_ID, CLIENT_SECRET)

for s in search_lst:
    out = sp.search(s, limit=1, offset=0, type='album', market=None)
    uri = out['albums']['items'][0]['id']
    img_url = out['albums']['items'][0]['images'][0]['url']
    album_name = out['albums']['items'][0]['name']
    img_data = requests.get(img_url).content
    with open(f'img/{album_name}.jpg', 'wb') as handler:
        _ = handler.write(img_data)
    print(f'{album_name}, {uri}, {img_url}')
```