import sys
import time
import threading

from gpiozero import Button
from sensors import photo_resistor, relay, soil_moisture
from libs.light import day_or_night


def loop_relays():
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        pump_water(relay_channel, flow_time = 5)


def pump_water(relay_channel, flow_time):
    # create a relay object.
    # Triggered by the output pin going low: active_high=False.
    # Initially off: initial_value=False
    try:
        relay.main_loop(relay.relay(relay_channel), flow_time)
    except KeyboardInterrupt:
        # turn the relay off
        relay.set_relay(False)
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)


def loop_from_soil_sensors():
    relay_channels = [4, 27, 22, 23]
    for analog_signal in range(0,4):
        soil_wet = soil_moisture.get_moisture(analog_signal)
        if soil_wet == 0:
            time.sleep(1)
            flow_time = 1
            pump_water(relay_channels[analog_signal], flow_time)
            time.sleep(1)


def button(pin, timeout):
    button_is_pressed = Button(pin).wait_for_press(timeout=timeout)
    if button_is_pressed:
        loop_relays()


def flow_calibration(flow_time):
    return flow_time


if __name__ == '__main__':
    timeout = 3600
    while True:
        light = day_or_night(place="brussels")
        light = 1
        if light == 1:
            thread_list = []
            soil_sensors_thread = threading.Thread(target=loop_from_soil_sensors, daemon=True)
            thread_list.append(soil_sensors_thread)
            flow_button = threading.Thread(target=button, args=(12, timeout), daemon=True)
            thread_list.append(flow_button)
            stop_button = threading.Thread(target=button, args=(6, timeout), daemon=True)
            thread_list.append(stop_button)
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
