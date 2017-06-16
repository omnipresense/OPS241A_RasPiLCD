#!/usr/bin/env python3

# Import time, decimal, serial, GPIO, reg expr, sys, and pygame modules
import os
import sys
from time import *
from decimal import *
import serial
import re
import pygame
from pygame.locals import *

# Ops241A module settings:  ftps, dir off, 5Ksps, min -9dB pwr, squelch 5000
Ops241A_Speed_Output_Units = 'UF'
Ops241A_Direction_Control = 'Od'
Ops241A_Sampling_Frequency = 'SV'
Ops241A_Transmit_Power = 'P0'
Ops241A_Threshold_Control = 'Q5'
Ops241A_Module_Information = '??'

# Display screen width and height
os.environ['SDL_VIDEODRIVER'] = 'fbcon'
os.environ["SDL_FBDEV"] = "/dev/fb1"
screen_size = (480, 300)
font_size = int(screen_size[1]/1.6)
font_type = "Calibri"
disp_velocity_header = "Time"


# Initialize pygame graphics and sound
# graphics
print("Initializing pygame graphics")
pygame.init()
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
screen = pygame.display.set_mode(screen_size)
screen_size_width = screen_size[0]
screen_size_height = screen_size[1]
pygame.display.set_caption("OmniPreSense Radar")
font = pygame.font.SysFont(font_type, font_size, True, False)
screen_bkgnd_color = BLACK
screen_bar_color = GREEN

# Initialize the display

velocity_col = int(screen_size[0] / 2.5)  # a bit left of center
velocity_row =  int(font_size * 0.3)  # nudge a bit

# Initialize the USB port to read from the OPS-241A module
ser=serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1,
    writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()

# sendSerialCommand: function for sending commands to the OPS-241A module
def sendSerCmd(descrStr, commandStr) :
    data_for_send_str = commandStr
    data_for_send_bytes = str.encode(data_for_send_str)
    print(descrStr, commandStr)
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
            
# Initialize and query Ops241A Module
print("\nInitializing Ops241A Module")
sendSerCmd("\nSet Speed Output Units: ", Ops241A_Speed_Output_Units)
sendSerCmd("\nSet Direction Control: ", Ops241A_Direction_Control)
sendSerCmd("\nSet Sampling Frequency: ", Ops241A_Sampling_Frequency)
sendSerCmd("\nSet Transmit Power: ", Ops241A_Transmit_Power)
sendSerCmd("\nSet Threshold Control: ", Ops241A_Threshold_Control)
sendSerCmd("\nModule Information: ", Ops241A_Module_Information)

ser=serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 0.01,
    writeTimeout = 2
    )


# Game Loop
done = False
while not done:
    screen.fill(screen_bkgnd_color)

    speed_available = False
    Ops241_rx_bytes = ser.readline()
    # Check for speed information from OPS241-A
    Ops241_rx_bytes_length = len(Ops241_rx_bytes)
    if (Ops241_rx_bytes_length != 0) :
        Ops241_rx_str = str(Ops241_rx_bytes)
        if Ops241_rx_str.find('{') == -1 :
            # Speed data found
            Ops241_rx_float = float(Ops241_rx_bytes)
            speed_available = True
    if speed_available == True :

        screen.fill(screen_bkgnd_color)

        # Render the text for display. "True" means anti-aliased text.
        velocity_rnd = round(Ops241_rx_float, 1)
        velocity_str = str(velocity_rnd)
        velocity_fr = font.render(velocity_str, True, WHITE)    
        screen.blit(velocity_fr, [velocity_col, velocity_row])

        # Update screen
        pygame.display.flip()
        # Limit to 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            