# Version: 1
# Written by Tim Hanewich

import network
import settings
import time

def try_connect(times:int = 10):

    CONNECTED = False
    TIMES_TRIED = 0

    while CONNECTED == False and TIMES_TRIED < times:

        # connect to wifi
        wlan = network.WLAN(network.STA_IF)
        print("Activitaing wlan...")
        wlan.active(True)
        print("Connecting...")
        wlan.connect(settings.ssid, settings.password)

        # wait a moment
        print("Waiting 3 seconds...")
        time.sleep(3)

        # check
        if wlan.isconnected():
            CONNECTED = True
            print("Connected to SSID '" + settings.ssid + "'!")
            ip = wlan.ifconfig()[0]
            return ip

        else:
            TIMES_TRIED = TIMES_TRIED + 1
            print("Connection to SSID '" + settings.ssid + "' failed on attempt # " + str(TIMES_TRIED))
        
    if CONNECTED == False:
        msg = "Failed to connect to SSID '" + settings.ssid + "' after " + str(TIMES_TRIED) + " attempts!"
        print(msg)
        raise Exception(msg)
    