#!/usr/bin/python

# Controls Artie3000 with WiiRemote via bluetooth.
# Connect a Nintendo Wii Remote via Bluetooth
# and read the button states in Python. Then it
# connects to Artie's websocket and sends commands.

# WiiRemote control based on:
# Project URL :
# https://www.raspberrypi-spy.co.uk/?p=1101
#
# Author : Matt Hawkins
# Date   : 30/01/2013

import asyncio, websockets
import cwiid
import time

button_delay = 0.1
buttons_prev = 0

async def send_ws_command():
    uri = "ws://192.168.0.80:8899/websocket"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(response)


print("Press 1 + 2 on your Wii Remote now ...")
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
    wii=cwiid.Wiimote()
except RuntimeError:
    print("Error opening wiimote connection")
    quit()
  
print("Wii Remote connected and ready...\n")
print("Press some buttons!\n")
print("Press PLUS and MINUS together to disconnect and quit.\n")

# Setting read-out mode
wii.rpt_mode = cwiid.RPT_BTN

while True:
 
    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed
    # together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print("\nClosing connection ...")
        wii.rumble = 1
        time.sleep(0.1)
        wii.rumble = 0
        time.sleep(0.1)
        wii.rumble = 1
        time.sleep(0.1)
        wii.rumble = 0
        time.sleep(0.1)
        wii.rumble = 1
        time.sleep(0.1)
        wii.rumble = 0
        exit(wii)
    
    # Check if other buttons are pressed by
    # doing a bitwise AND of the buttons number
    # and the predefined constant for that button.
    if (buttons != buttons_prev):
        if (buttons & cwiid.BTN_UP):
            print("Up pressed")
            command = "forward"
#            time.sleep(button_delay)

        if (buttons & cwiid.BTN_DOWN):
            print("Down pressed")
            command = "back"

        if (buttons & cwiid.BTN_LEFT):
            print("Left pressed")
            command = "left"

        if (buttons & cwiid.BTN_RIGHT):
            print("Right pressed")
            command = "right"

        if (buttons & cwiid.BTN_A):
            print("A pressed")
            
            wii.rumble = 1
            time.sleep(0.05)
            wii.rumble = 0
            
            wii.led = 0
            command = "penup"

        if (buttons & cwiid.BTN_B):
            print("B pressed")
            
            wii.rumble = 1
            time.sleep(0.05)
            wii.rumble = 0
            
            wii.led = cwiid.LED4_ON
            command = "pendown"

        if (buttons == 0):
            print("Buttons released")
            command = "stop"
 #           time.sleep(button_delay)
        
        message = "{\"cmd\": \"" + command + "\",\"arg\": 9999}"
        asyncio.get_event_loop().run_until_complete(send_ws_command())
    
    buttons_prev = buttons

