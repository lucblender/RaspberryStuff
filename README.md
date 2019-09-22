# Raspberry Stuff

This git has for purpose to describe many different work about Raspberry and the aditional hardware I used with it.

You can find 3 folders:

## LCD
- Use of the pitft capacitive touchscreen by adafruit
- S2PI screen
- X11Vnc configuration
## Mus-ink Box (A music box project featuring)
- Audio configuration with alsa and pulse audio
    - Purpose to create a loopback audio card to capture played audio 
- Support of mopidy 
- Support of librespot
- E-Ink display 
    - 5.83'' 2.7'' red and black from waveshare
    - Show the actual music played on mopidy and librespot
- Vumeter made with neopixels
- Full system launch using systemctl service
## homeAutomation
Home automation system for Raspberry Pi using:
- Zwave.me, OpenHab, MyOpenHab
    - For devices binding and use with GoogleHome
- InfluxDb (using docker) and Grafana
    - Persistence and visualisation of data