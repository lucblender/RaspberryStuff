
let upSeconds="$(/usr/bin/cut -d. -f1 /proc/uptime)"
let secs=$((${upSeconds}%60))
let mins=$((${upSeconds}/60%60))
let hours=$((${upSeconds}/3600%24))
let days=$((${upSeconds}/86400))
UPTIME=`printf "%d days, %02dh%02dm%02ds" "$days" "$hours" "$mins" "$secs"`
read one five fifteen rest < /proc/loadavg

echo "$(tput setaf 6)    __  ___                     _         __  $(tput setaf 4)    ____
$(tput setaf 6)   /  |/  /__  __ _____        (_)____   / /__$(tput setaf 4)   / __ ) ____   _  __
$(tput setaf 6)  / /|_/ // / / // ___/______ / // __ \ / //_/$(tput setaf 4)  / __  |/ __ \ | |/_/
$(tput setaf 6) / /  / // /_/ /(__  )/_____// // / / // ,<   $(tput setaf 4) / /_/ // /_/ /_>  <
$(tput setaf 6)/_/  /_/ \__,_//____/       /_//_/ /_//_/|_| $(tput setaf 4) /_____/ \____//_/|_|$(tput setaf 7)
--------------------------------------------------------------------
Uptime.............: ${UPTIME}
Ram................: $(free -m | awk 'NR==2 { printf "Total: %sMB, Used: %sMB, Free: %sMB",$2,$3,$4; }')
Disk Memory........: $(df -h ~ | awk 'NR==2 { printf "Total: %sB, Used: %sB, Free: %sB",$2,$3,$4; }')
Load Averages......: ${one}, ${five}, ${fifteen} (1, 5, 15 min)
Running Processes..: `ps ax | wc -l | tr -d " "`
--------------------------------------------------------------------
$(tput sgr0)"
