# PiMusicBox and Mopidy


## PiMusicBox Config

- line 18-19 wifi
- line 48 enable-ssh      username root password musicbox
- line 64 Spotify         Client id for modipy https://www.mopidy.com/authenticate/
- line 81 Spoitfy Web
- line 244 Spotify Connect

## Requirement

The mopidyapi is used to have access to the JSON RPC mopidy api. Watchdog library is used to watchdog the librespot logs file

```
pip3 install mopidyapi
pip3 install watchdog
```
To note, it use is compatible with python 3.6 and higher. To install python 3.6 on raspberry-pi, you can refer to: 

http://www.knight-of-pi.org/installing-python3-6-on-a-raspberry-pi/


## Update for spotify connect (Librespot)
If for some reason the spotify connect on PiMusicBox doesn't work, you can update librespot with the following commands:

```
service librespot stop
cd /opt/librespot
wget https://github.com/pimusicbox/librespot/releases/download/v20180529-1e69138/librespot-linux-armhf-raspberry_pi.zip
unzip librespot-linux-armhf-raspberry_pi.zip
rm librespot-linux-armhf-raspberry_pi.zip
service librespot start
```
### Lauch Librespot with logs file
```
./librespot -b 320 -v -c /tmp --name 'RaspberryPi MusicBox' >/root/mopidyapi/data/librespotOutput 2>&1
```
When lauched as described and not as service, you can use mopidyTrackInfoPatch.py to also show music played with spotify connect.
## mopidyTrackInfoPatch.py

This script can show the current track played on mopidy (pimusic box) and spotify connect (librespot). It will be displayed on a 5.3'' e-ink display.
You'll have to use musicDisplay.py, epd5in83b.py and epdconfig.py from E-Ink\e-Paper\5.83inch_e-paper_b&c_code\*, and imageDivider.py from E-Ink\*

**For now the mopidyapi library has a bug that doesn't let me use the pip version. Please install mopidyapi by cloning its git and change the line 84 in httpclient.py from  ```return deserialize_mopidy(r['result'])``` to ```return r```**