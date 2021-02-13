import sys
import time

from gpiozero import Button
from sensors import photo_resistor, relay


while True:
    photo_resistor.get_light(13, 26)
    time.sleep(1)
    resistance = photo_resistor.get_light(13, 26)
    normalized_light = photo_resistor.normalize_light(resistance)
    print(r"Light (from 0 to 1): "+str(round(normalized_light,2)))
    if normalized_light < 0.1 or Button(12).wait_for_press(timeout = 600):
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
    else:
        continue
