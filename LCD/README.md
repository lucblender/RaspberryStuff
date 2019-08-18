# LCD & X11VNC

LCD models:
- pitft capacitive 2.8''
- 7 Inch 1024x600 Capacitive Touch Screen DIY Kit by S2PI
    
## LCD

### Pitft
https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/blob/master/adafruit-pitft.sh

### S2PI screen
If any resolution problem in ```/boot/config.txt``` add:
```
hdmi_force_hotplug=1 
hdmi_group=2 
hdmi_mode=87 
hdmi_cvt 1024 600 60 3 0 0 0
``` 

## X11VNC

Install x11vnc and xorg dummy video driver to use x11vnc without screen:


``` 
sudo apt-get install x11vnc
sudo apt-get install xserver-xorg-video-dummy
``` 

Create a x11vnc password:
sudo apt-get install xserver-xorg-video-dummy



``` 
x11vnc -storepasswd "mypassword" ~/.vnc_passwd
``` 

Create Xorg configuration file in ``` /usr/share/X11/xorg.conf.d/xorg.conf/xorg.conf```:
```
Section "Device"
    Identifier  "Configured Video Device"
    Driver      "dummy"
EndSection

Section "Monitor"
    Identifier  "Configured Monitor"
    HorizSync 31.5-48.5
    VertRefresh 50-70
EndSection

Section "Screen"
    Identifier  "Default Screen"
    Monitor     "Configured Monitor"
    Device      "Configured Video Device"
    DefaultDepth 24
    SubSection "Display"
    Depth 24
    Modes "1920x1080"
    EndSubSection
EndSection
```


Create a service to launch x11vnc at startup on ```/etc/systemd/system/x11vnc.service```

```
[Unit]
Description=VNC Server for X11
Requires=display-manager.service

[Service]
ExecStart=/usr/bin/x11vnc -auth "authpath" -display :0 -rfbauth "passwordpath" -shared -forever
ExecStop=/usr/bin/x11vnc -R stop
Restart=on-failure
RestartSec=2
User=root

[Install]
WantedBy=multi-user.target
``` 

- authpath: ```ps wwwwaux | grep auth``` 
- passwordpath: path set when used x11vnc -storepasswd 
