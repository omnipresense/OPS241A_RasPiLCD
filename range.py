#!/usr/bin/python3

# Import time, decimal, serial, GPIO, reg expr, sys, and pygame modules
import os
import sys
from time import *
from decimal import *
import serial
import re
import pygame
from pygame.locals import *
import colorsys
import pdb

# Ops241B module settings:  ftps, dir off, 5Ksps, min -9dB pwr, squelch 5000
Ops241B_Output_Units_OFF = 'Ou'
Ops241B_Output_Magnitude_ON = 'OM'
Ops241B_Range_Output_Units = 'uM'
Ops241B_Wait_Interval = 'WL'
Ops241B_Transmit_Power = 'PD'    # miD power
Ops241B_Threshold_Control = 'm>200/r/n'
Ops241B_Reporting_Preference = 'Ov' # OV is oprder by the value.  /=sm to lg`
#Ops241B_Reporting_Preference = 'OVO\\' # OV is oprder by the value.  /=sm to lg`
Ops241B_Module_Information = '??'

logo_height = 65
logo_width = 300

use_LCD=True
if use_LCD:
    # Display screen width and height
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    screen_size = (320, 240)
else:
    print("Not configured for TFT display")
    #screen_size = (1280, 720)
    screen_size = (640, 480)




# Initialize pygame graphics and sound
# graphics
print("Initializing pygame graphics")
pygame.init()
pygame.display.init()
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
screen = pygame.display.set_mode(screen_size)
screen_size_width = screen_size[0]
screen_size_height = screen_size[1]
units_lbl_font_size = int(screen_size_width/10)
pygame.display.set_caption("OmniPreSense Radar")

# Initialize the display
screen_bkgnd_color = (0x30,0x39,0x86)
screen.fill(screen_bkgnd_color)
logo = pygame.image.load('/home/pi/ops_logo_300x65.jpg')
logo_x = (screen_size_width - 300 )/2
screen.blit(logo, (logo_x,1))  # (320-300)/2

range_font_size = 120
range_font_name = "Consolas"
range_font = pygame.font.SysFont(range_font_name, range_font_size, True, False)
range_col = int(screen_size[0] / 4)  # quarter of the way in
range_row = logo_height + int(range_font_size * 0.3)  # nudge a bit

units_lbl_font = pygame.font.SysFont(range_font_name, units_lbl_font_size, True, False)
units_lbl = units_lbl_font.render("meters", True, WHITE)    
units_lbl_col = int(screen_size[0] *  (0.63))  # most of the way in
units_lbl_row = (range_row + range_font_size) - (2*units_lbl_font_size)
screen.blit(units_lbl, [units_lbl_col, units_lbl_row])

# Update screen
pygame.display.flip()


# sendSerialCommand: function for sending commands to the OPS-241B module
def send_serial_cmd(print_prefix, command) :
    data_for_send_str = command
    data_for_send_bytes = str.encode(data_for_send_str)
    print(print_prefix, command)
    ser.write(data_for_send_bytes)
    # Initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # Print out module response to command string
    while not ser_write_verify :
        data_rx_bytes = ser.readline()
        data_rx_length = len(data_rx_bytes)
        if (data_rx_length != 0) :
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start) :
                ser_write_verify = True
            
# Initialize the USB port to read from the OPS-241B module
ser=serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1,
    writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()
# Initialize and query Ops241B Module
print("\nInitializing Ops241B Module")
send_serial_cmd("\nModule Information: ", Ops241B_Module_Information)
send_serial_cmd("\nSet Wait interval: ", Ops241B_Wait_Interval)
send_serial_cmd("\nSet Range Output Units to Meters: ", Ops241B_Range_Output_Units)
send_serial_cmd("\nSet Reporting order pref (by mag or distance): ", Ops241B_Reporting_Preference)
send_serial_cmd("\nSet Output Units OFF: ", Ops241B_Output_Units_OFF)
send_serial_cmd("\nSet Magnitude Output ON: ", Ops241B_Output_Magnitude_ON)
#send_serial_cmd("\nSet Transmit Power: ", Ops241B_Transmit_Power)
#send_serial_cmd("\nSet Threshold Control: ", Ops241B_Threshold_Control)


# Main Loop
def read_and_render():
    MAX_HUE = 300 # use color wheel from 0 - 300
    max_discovered_mag = 500
    done = False
    while not done:
        range_available = False
        Ops241_rx_bytes = ser.readline()
        # Check for range information from OPS241
        Ops241_rx_bytes_length = len(Ops241_rx_bytes)
        if (Ops241_rx_bytes_length != 0) :
            Ops241_rx_str = Ops241_rx_bytes.decode("utf-8")
            #print("RX:"+Ops241_rx_str)
            if len(Ops241_rx_str) > 3 and Ops241_rx_str.find('{') == -1 :
                # Speed data found
                try:
                    maybe_nums = Ops241_rx_str.split(',')
                    Ops241_mag_float = float(maybe_nums[0])
                    Ops241_range_float = float(maybe_nums[1])
                    range_available = True

                    # color is proportional to the max mag ever seen
                    if Ops241_mag_float > max_discovered_mag:
                        max_discovered_mag = Ops241_mag_float 
                        # though note that it permanenty changes, until restart
                except ValueError:
                    print("Unable to convert the strings {} and {}".format(maybe_nums[0],maybe_nums[1]) )
                    range_available = False
    
        if range_available == True :
            pygame.draw.rect(
                screen,
                screen_bkgnd_color, 
                (range_col,range_row,screen_size_width-range_col,range_font_size),
                0)
            
            range_rnd = round(Ops241_range_float, 1)
            range_str = str(range_rnd)
            hue = 1 - (Ops241_mag_float / max_discovered_mag)  # so peak = 0, dim = 1
            hue *= (MAX_HUE / 360)  # discard wheel portion from violet back to red
            color_to_render = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            range_rend = range_font.render(range_str, 
                True, # Render the text for display. "True" means anti-aliased text.
                (255*color_to_render[0],255*color_to_render[1],255*color_to_render[2]))
            screen.blit(range_rend, [range_col, range_row])
            screen.blit(units_lbl, [units_lbl_col, units_lbl_row])
    
            # Update screen
            pygame.display.flip()
            # Limit to 60 frames per second
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                

read_and_render()
