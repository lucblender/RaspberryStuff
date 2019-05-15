# Audio Configuration

https://www.pimusicbox.com

## Dependency 
### install alsaaudio for python

sudo apt-get install libasound2-dev
sudo pip3 install pyalsaaudio --user

### for pactl and pulesaudio
sudo apt-get install pulseaudio-utils 
sudo apt-get install pulseaudio

### Loopback card
## add loopback card temporarly
modprobe snd-aloop
## add loopback card at each boot
in /etc/modules add snd-aloop

### Play audio on specific card
aplay -D "hw:Loopback" 01\ Somebody\ to\ Shove.wav

### Source of vumeter.py 
https://github.com/andrebispo5/VumeterRasPi


### Usefull audio command

- aplay -l
- cat /proc/asound/cards
- pactl list short sinks



### Modification on pulesaudio config

sudo nano /etc/pulse/default.pa

## Remove Idle status on cards
To comment:
```
### Automatically suspend sinks/sources that become idle for too long"
#load-module module-suspend-on-idle
```
## Create a combined card of hardware and loopback card
To add:
```
load-module module-alsa-sink device="hw:0,0" sink_name=hardware_card
load-module module-alsa-sink device="hw:Loopback,1,1" sink_name=loopback_card
load-module module-combine-sink sink_name=hardware_loopback_mix_card slaves=hardware_card,loopback_card
set-default-sink hardware_loopback_mix_card
```
## Make this combined card (n°4) default
```
set-default-sink 4
set-default-source 4
```
