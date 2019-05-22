# PiMusicBox and Mopidy


## PiMusicBox Config

line 18-19 wifi
line 48 enable-ssh      username root password musicbox
line 64 Spotify         Client id for modipy https://www.mopidy.com/authenticate/
line 81 Spoitfy Web
line 244 Spotify Connect

## Requirement

The mopidyapi is used to have access to the JSON RPC mopidy api.

```
pip3 install mopidyapi
```
To note, it use is compatible with python 3.6 and higher. To install python 3.6 on raspberry-pi, you can refer to: 

http://www.knight-of-pi.org/installing-python3-6-on-a-raspberry-pi/


## Update for spotify connect
If for some reason the spotify connect on PiMusicBox doesn't work, you can update librespot with the following commands:

```
service librespot stop
cd /opt/librespot
wget https://github.com/pimusicbox/librespot/releases/download/v20180529-1e69138/librespot-linux-armhf-raspberry_pi.zip
unzip librespot-linux-armhf-raspberry_pi.zip
rm librespot-linux-armhf-raspberry_pi.zip
service librespot start
```