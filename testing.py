import photo_diode, relay
import sys
import time

while True:
    error = 1
    normalized_light_i = 0
    normalized_light_ii = 0
    i = 0
    while error > 0.075 and i > 3:
        normalized_light_i = resistance = photo_diode.get_light(13, 26)
        time.sleep(0.05)
        normalized_light = photo_diode.normalize_light(resistance)
        error = abs(normalized_light_i - normalized_light_ii)
        print(normalized_light)
        i = i + 1
    if normalized_light > 0.9:
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
