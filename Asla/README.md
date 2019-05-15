### Audio Configuration

https://www.pimusicbox.com


sudo pip3 install pyalsaaudio --user

modprobe snd-aloop
--> or for each boot : snd-aloop in /etc/modules

aplay -D "hw:Loopback" 01\ Somebody\ to\ Shove.wav


https://github.com/andrebispo5/VumeterRasPi



https://julip.co/2012/05/arduino-python-soundlight-spectrum/


aplay -l
cat /proc/asound/cards
pactl list short sinks


adafruit : https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

sudo nano /etc/pulse/default.pa
### Make some devices default
set-default-sink 0
set-default-source 0

sudo apt-get install gnome-control-center
https://askubuntu.com/questions/78174/play-sound-through-two-or-more-outputs-devices