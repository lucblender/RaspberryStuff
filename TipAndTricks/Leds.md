# Turn off leds on a Raspberry Pi using /sys/class

_May need ```sudo su```!_ 

You can adapt it to your need, if you want to turn on just replace the 0 by 255 or the 255 by 0 and you can change the trigger; ``` cat /sys/class/leds/ledX/trigger``` to list all available triggers.

## Pi 1 B Rev. 2 
```
echo none > /sys/class/leds/led0/trigger
echo 0 > /sys/class/leds/led0/brightness
```

## Pi zero
```
echo none > /sys/class/leds/led0/trigger
echo 255 > /sys/class/leds/led0/brightness
```
## Pi 3b & 3b+ 
```
echo none > /sys/class/leds/led0/trigger
echo 0 > /sys/class/leds/led0/brightness
echo none > /sys/class/leds/led1/trigger
echo 0 > /sys/class/leds/led1/brightness
```
