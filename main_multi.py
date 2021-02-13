import sys
import time

from gpiozero import Button
from sensors import photo_resistor, relay
from multiprocessing import Process


def loop_relays(relay):
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        # create a relay object.
        # Triggered by the output pin going low: active_high=False.
        # Initially off: initial_value=False
        try:
            relay.main_loop(relay.relay(relay_channel))
        except KeyboardInterrupt:
            # turn the relay off
            relay.set_relay(False)
            print("\nExiting application\n")
            # exit the application
            sys.exit(0)

def loop_from_light():
    while True:
        photo_resistor.get_light(13, 26)
        time.sleep(0.25)
        resistance = photo_resistor.get_light(13, 26)
        normalized_light = photo_resistor.normalize_light(resistance)
        if normalized_light < 0.1:
            loop_relays(relay)
        else:
            time.sleep(0.25)
            continue


def loop_from_button(Button, relay):
    while True:
        button_is_pressed = Button(12).wait_for_press(timeout=600)
        if button_is_pressed:
            loop_relays(relay)
        else:
            time.sleep(0.25)
            continue

if __name__ == '__main__':
    first = Process(target=loop_from_light, args=())
    second = Process(target=loop_from_button, args=(Button, relay))


