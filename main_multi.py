import sys
import time

from gpiozero import Button
from sensors import photo_resistor, relay, soil_moisture
from multiprocessing import Process


def loop_relays(relay):
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        # create a relay object.
        # Triggered by the output pin going low: active_high=False.
        # Initially off: initial_value=False
        pump_water(relay_channel)


def pump_water(relay_channel, flow_time):
    try:
        relay.main_loop(relay.relay(relay_channel), flow_time)
    except KeyboardInterrupt:
        # turn the relay off
        relay.set_relay(False)
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)


def loop_from_soil_sensors():
    while True:
        relay_channels = [4, 27, 22, 23]
        for analog_signal in range(0,4):
            soil_wet = soil_moisture.get_moisture(analog_signal)
            if soil_wet == 0:
                time.sleep(1)
                flow_time = 5
                pump_water(relay_channels[analog_signal], flow_time)
                time.sleep(1)
            else:
                time.sleep(1)
                continue
        time.sleep(900)


def loop_from_button(Button, relay):
    while True:
        button_is_pressed = Button(12).wait_for_press(timeout=600)
        if button_is_pressed:
            loop_relays(relay)
        else:
            time.sleep(0.25)
            continue

if __name__ == '__main__':
    # second = Process(target=loop_from_button, args=(Button, relay))
    # third = Process(target=loop_from_soil_sensors, args=(Button, relay))
    while True:
        loop_from_soil_sensors()



