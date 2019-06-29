To root's crontab (sudo crontab -e)
```
@reboot /usr/bin/python3 /home/pi/ops_radar.py > /home/pi/ops_radar_cron_startup.log
* * * * * /home/pi/radar_restarter.sh
```

Ensure that ops_radar.py is the program you want.  
This time, I made hard links into OPS241A_RasPiLCD/range.py
```
ln OPS241A_RasPiLcd/range.py ops_radar.py
```
and use speed.py if that's what the connected sensor will be 

Starting the radar immediately (@reboot) is nice for quick startup.  
Then launch radar_restarter.sh which  runs every minute.  The script elegantly looks for ops_radar.py (pgrep -f)
If running, it exits.  If not, it rolls logs over, starts again, etc
