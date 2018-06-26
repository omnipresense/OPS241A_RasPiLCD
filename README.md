## OmniPreSense RADAR for Raspberry Pi LCD screens

This repo has an implementation of a short python program that reads
radar reports from OmniPreSense OPS-241x radar units and displays
them on the screen.  (The screen most likely being a small LCD attached 
to a Raspberry Pi.)

The OmniPreSense radar sensor reports velocity data to any computer 
attached to its on-board USB port.  (It uses USB CDC mode)

The program does a bit of configuration and then data massaging to blit it 
out to the display.

### Installation and configuration

Technically the python script does not care where it is run from.  
This repo also has a single line execution script, named run_radar.sh, 
typically placed in /home/pi, which then runs the python script. 
This script expects the python script to be in a folder matching this repo 
name.  This allows one to simply 

```
git clone https://github.com/omnipresense/OPS241A_RasPiLCD.git
```

(and ```mv run_radar.sh /home/pi``` and ```chmod 755 /home/pi/run_radar.sh```)

The next trick is to get it to auto-run

A graphical front end must be running, and the default for Raspian these days
is LXDE.   

To have the radar start at system boot time, the file 
```
/home/pi/.config/lxsession/LXDE-pi/autostart
```
must have an line that is (approximately)
```
@/home/pi/run_radar.sh
```

You probably want to manipulate the LX menus that come up by default to be relevant to a 480x300 display intended to demonstrate the radar.  This means disabling almost everything except a new entry for the radar, which will call the run_radar.sh script.
The most reliable way to do this is using the window menu system that you see on the screen (or via VNC, see below)

#### Tips
VNC can be helpful for seeing the pi display on a PC.
It can be enabled by ```sudo raspi-config```
However, there are strange permissions that must be corrected for. 
```
sudo vi /root/.vnc/config.d/vncserver-x11
Authentication=VncAuth
sudo vncpasswd -service
```

An alternative, perhaps better than the one that comes with the pi, is to use tightvnc ``sudo apt-get install tightvnccserver``` because it is possible to have a remote display not limited to the size of the LCD screen.  


 
