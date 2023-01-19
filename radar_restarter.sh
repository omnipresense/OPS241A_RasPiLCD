#!/bin/sh

#while `true`
#do
    if pgrep -f ops_radar.py ; then
        echo "found ops_radar.py.  exiting."
        exit
    else
        echo copy recent log
        if [ -f "/home/pi/radar_restarter.log" ] ; then
            cp "/home/pi/radar_restarter.log" "/home/pi/radar_restarter.log.bck"
        fi

        #echo wait while echo is turned off
        #/usr/bin/python serial_util.py --timeToLive 2

        echo "launching radar, with output sent to ~/radar_restarter.log"
        cd /home/pi
        /usr/bin/python3 /home/pi/ops_radar.py > /home/pi/radar_restarter.log 2>&1
        echo If you are seeing this earlier than expected, try to run it manually via 'sudo python3 ~/pi/ops_radar.py'
        sleep 1
    fi
#done
