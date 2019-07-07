# Mopidy (spotify) and librespot

## Requirement

The mopidyapi is used to have access to the JSON RPC mopidy api. Watchdog library is used to watchdog the librespot logs file

```
pip3 install mopidyapi
pip3 install watchdog
```
To note, it use is compatible with python 3.6 and higher. To install python 3.6 on raspberry-pi, you can refer to: 

http://www.knight-of-pi.org/installing-python3-6-on-a-raspberry-pi/

### Build librespot

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
When lauched as described and not as service, you can use mopidyTrackInfo.py to also show music played with spotify connect.
## mopidyTrackInfo.py

This script can show the current track played on mopidy (pimusic box) and spotify connect (librespot). It will be displayed on a 5.3'' or 2.7'' e-ink display.