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


def activate_relay_for_time(port_number, time):
    set_relay(True, relay_pin)
    time.sleep(time)
    toggle_relay(relay_pin)
    time.sleep(0.25)


def activate_relays_in_sequence(relay_ports, time):
    for relay_port in relay_ports:
        activate_relay_for_time(relay_port, time)


def testing_loop(relay_pin):
    # start by turning the relay off
    set_relay(False, relay_pin)
    while 1:
        # then toggle the relay every second until the app closes
        toggle_relay()
        # wait a second
        time.sleep(1)


if __name__ == "__main__":
    relay_pin = 4
    try:
        testing_loop(relay_pin)
    except KeyboardInterrupt:
        # turn the relay off
        set_relay(False, relay_pin)
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)



relay_channels = [4, 22, 23, 27]
for channel in relay_channels:
    set_relay(True, channel)


