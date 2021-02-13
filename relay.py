#!/usr/bin/python

# A simple Python application for controlling a relay board from a Raspberry Pi
# The application uses the GPIO Zero library (https://gpiozero.readthedocs.io/en/stable/)
# The relay is connected to one of the Pi's GPIO ports, then is defined as an Output device
# in GPIO Zero: https://gpiozero.readthedocs.io/en/stable/api_output.html#outputdevice

import sys
import time

import gpiozero


def set_relay(status, relay):
    if status:
        print("Setting relay: ON")
        relay.on()
    else:
        print("Setting relay: OFF")
        relay.off()


def toggle_relay(relay):
    print("toggling relay")
    relay.toggle()


def main_loop(relay):
    # start by turning the relay off
    set_relay(False, relay)
    start_time = time.time()
    end_time = 0
    while end_time < 4.5:
        # then toggle the relay every second until the app closes
        toggle_relay(relay)
        # wait a second 
        time.sleep(1)
        end_time = start_time - time.time()


if __name__ == "__main__":
    relay_channels = [4, 22, 23, 27]
    for relay_channel in relay_channels:
        # create a relay object.
        # Triggered by the output pin going low: active_high=False.
        # Initially off: initial_value=False
        relay = gpiozero.OutputDevice(relay_channel, active_high=False, initial_value=False)
        try:
            main_loop(relay)
        except KeyboardInterrupt:
            # turn the relay off
            set_relay(False)
            print("\nExiting application\n")
            # exit the application
            sys.exit(0)