# wifi-task.sh

This little bash script try to ping google.com to determine if the wifi is down. If so, it will restart the wlan0 interface.


## Run with cron

add this line to your crontab if you want to make it run every 5 minutes and output the log to a files:

```*/5 * * * * /bin/bash /home/pi/wifi-task.sh >> wifi-task.log 2>&1```