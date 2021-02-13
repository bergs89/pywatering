import sys
import time

import gpiozero

def set_relay(status, relay_pin):
    relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False)
    if status:
        print("Setting relay: ON")
        relay.on()
    else:
        print("Setting relay: OFF")
        relay.off()


def toggle_relay(relay_pin):
    relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False)
    print("toggling relay")
    relay.toggle()

if __name__ == "__main__":
    relay_pin = 4
    try:
        toggle_relay(relay_pin)
    except KeyboardInterrupt:
        # turn the relay off
        set_relay(False, relay_pin)
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)