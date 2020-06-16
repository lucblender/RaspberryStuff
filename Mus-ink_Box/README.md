``` 
    __  ___                     _         __      ____
   /  |/  /__  __ _____        (_)____   / /__   / __ ) ____   _  __
  / /|_/ // / / // ___/______ / // __ \ / //_/  / __  |/ __ \ | |/_/
 / /  / // /_/ /(__  )/_____// // / / // ,<    / /_/ // /_/ /_>  <
/_/  /_/ \__,_//____/       /_//_/ /_//_/|_|  /_____/ \____//_/|_|
```

## Descriptions

## Dependency 

For the dependency, please refer to the "Componant README" folder. Since this system is modular, it is better to refer to those different readme if you want to install only one part of the system. 

## Configuration

A configuation file can be found in ./workspace/conf/musinkConfig.conf

Here is the available configuration, it is useful to change the vumeter style (change are dynamic), the size of the e-ink display and the mopidy server in use.
 
```
#Parameters for the vumeter
#To note that the vumeter configuration is dynamic and will affect immediatly the leds
[vumeter]
enable=True
turningColor=True 
allLedSame=False
doFFT=True
onlyRed=False
ledsNumber=16

#The e-ink code works with either 2.7inch or 5.83inch
#If smallScreen is enabled --> will use the 2.7inch e-ink
[e-ink]
smallScreen=True

[mopidy]
host=localhost
port=6680
```

## Services

All the system is launched using systemd service. The services are the followings:
- einkMopidyLibrespot.service
    - will run the python code used for the e-ink
- librespot.service
    - will run librespot and redirect it's output to a log file in ./workspace/data
- mopidyCustom.service
    - will run mopidy, it's different than the usual mopidy service since linked to librespot service to launch
- pulseAudio.service
    - will run pulseaudio
- vumeter. service 
    - will run the python code that use neopixel as vumeter


## Motd

An custom Motd for your raspberry pi is available in the file motd.sh, you have to copy it in your /etc/profile.d folder. You can also remove the /etc/motd file for better esthetic.

Credits goes to:

https://www.raspberrypi.org/forums/viewtopic.php?t=23440

https://github.com/gagle/raspberrypi-motd

## Example

The screen example folder contain pictures that represent the e-ink display. Here are two examples out of the 6 availables:

![2.7inch screen](https://github.com/lucblender/RaspberryStuff/blob/master/Mus-ink_Box/ScreenExample/e-ink2.7Mopidy.png)

![5.83 inches screen](https://github.com/lucblender/RaspberryStuff/blob/master/Mus-ink_Box/ScreenExample/e-ink5.83Spotify.png)
