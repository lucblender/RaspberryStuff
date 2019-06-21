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


## Update for spotify connect 
### For mopidy(Librespot)
If for some reason the spotify connect on PiMusicBox doesn't work, you can update librespot with the following commands:

```
service librespot stop
cd /opt/librespot
wget https://github.com/pimusicbox/librespot/releases/download/v20180529-1e69138/librespot-linux-armhf-raspberry_pi.zip
unzip librespot-linux-armhf-raspberry_pi.zip
rm librespot-linux-armhf-raspberry_pi.zip
service librespot start
```
### Disabled in mopidy and build latest version

```
sudo apt-get install build-essential libasound2-dev         //needed to build libresport
curl https://sh.rustup.rs -sSf | sh                         // install rust and so cargo (also needed for build)
git clone https://github.com/librespot-org/librespot.git
cd librespot
cargo build --release                                       //actual build
```

### Lauch Librespot with logs file
```
./librespot -b 320 -v -c /tmp --name 'RaspberryPi MusicBox' >/home/pi/workspace/data/librespotOutput 2>&1
```
When lauched as described and not as service, you can use mopidyTrackInfoPatch.py to also show music played with spotify connect.
## mopidyTrackInfoPatch.py

This script can show the current track played on mopidy (pimusic box) and spotify connect (librespot). It will be displayed on a 5.3'' e-ink display.
You'll have to use musicDisplay.py, epd5in83b.py and epdconfig.py from E-Ink\e-Paper\5.83inch_e-paper_b&c_code\*, and imageDivider.py from E-Ink\*