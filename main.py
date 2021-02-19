import sys
import time
import threading

from gpiozero import Button
from sensors import photo_resistor, relay, soil_moisture
from libs.light import day_or_night


def loop_relays(flow_time):
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        pump_water(relay_channel, flow_time)


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


def loop_from_soil_sensors(flow_time):
    relay_channels = [4, 27, 22, 23]
    for analog_signal in range(0,4):
        soil_wet = soil_moisture.get_moisture(analog_signal)
        if soil_wet == 0:
            time.sleep(1)
            pump_water(relay_channels[analog_signal], flow_time)
            time.sleep(1)


def flow_button(pin, timeout):
    start_time = time.time()
    total_time = 0
    while total_time < timeout:
        button_is_pressed = Button(pin).wait_for_press(timeout=timeout)
        if button_is_pressed:
            loop_relays(flow_time)
        total_time = time.time() - start_time


def stop_button(pin, timeout, thread_list):
    start_time = time.time()
    total_time = 0
    stop_button_pressed = 0
    while total_time < timeout:
        button_is_pressed = Button(pin).wait_for_press(timeout=timeout)
        if button_is_pressed:
            stop_button_pressed = True
            # for thread in thread_list:
            #     thread._Thread_stop()
            sys.exit()
        total_time = time.time() - start_time
    return stop_button_pressed


def flow_calibration(flow_time):
    return flow_time


if __name__ == '__main__':
    timeout = 3600
    flow_time = 2
    while True:
        thread_list = []
        light = day_or_night(place="brussels")
        if light == 1:
            soil_sensors_thread = threading.Thread(target=loop_from_soil_sensors, args=(flow_time, ), daemon=True)
            thread_list.append(soil_sensors_thread)
        flow_button = threading.Thread(target=flow_button, args=(12, timeout), daemon=True)
        thread_list.append(flow_button)
        stop_button_pressed = threading.Thread(target=stop_button, args=(6, timeout, thread_list), daemon=True)
        thread_list.append(stop_button_pressed)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
