# Audio Configuration

https://www.pimusicbox.com

## Dependency 
### install alsaaudio for python
```
sudo apt-get install libasound2-dev
sudo pip3 install pyalsaaudio --user
```

### For pactl and pulesaudio
```
sudo apt-get install pulseaudio-utils 
sudo apt-get install pulseaudio
```

## Loopback card
### add loopback card temporarly
```
modprobe snd-aloop
```
### add loopback card at each boot
in /etc/modules add *snd-aloop*

## Play audio on specific card
```
aplay -D "hw:Loopback" 01\ Somebody\ to\ Shove.wav
```




## Usefull audio command

- aplay -l
- cat /proc/asound/cards
- pactl list short sinks



## Modification on pulesaudio config

sudo nano /etc/pulse/default.pa

### Remove Idle status on cards
To comment:
```
### Automatically suspend sinks/sources that become idle for too long
#load-module module-suspend-on-idle
```
### Create a combined card of hardware and loopback card

The combined card will mix the loopback card created before and the *hw:0,0* card. Consider changing this to match your own hardware.

To add:
```
load-module module-alsa-sink device="hw:0,0" sink_name=hardware_card
load-module module-alsa-sink device="hw:Loopback,1,1" sink_name=loopback_card
load-module module-combine-sink sink_name=hardware_loopback_mix_card slaves=hardware_card,loopback_card
set-default-sink hardware_loopback_mix_card
```
### Make this combined card default
With audio command I can find that n°4 is hardware_loopback_mix_card
```
set-default-sink 4
set-default-source 4
```

## Vumeter

The vumeter.py code will connect to the loopback_card, sample the audio and represent it on a vumeter made with neopixels. For more info about neopixels please check Neopixels folder to the root of this repository.

The fact that we created a mix card and put is as default mean our audio will always go on the physical card choosen and on the loopback card.

### Source of vumeter.py 
https://github.com/andrebispo5/VumeterRasPi

### Launch code

Since we are using the board python module, we need to launch the code with root privilege. 

```
sudo python3 vumeter.py
```