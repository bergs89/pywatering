import sys
import time
import threading

from datetime import datetime, timezone
from datetime import timedelta
from gpiozero import Button
from sensors import photo_resistor, relay, soil_moisture
from multiprocessing import Process
from libs.light import day_or_night

def loop_relays():
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        # create a relay object.
        # Triggered by the output pin going low: active_high=False.
        # Initially off: initial_value=False
        pump_water(relay_channel, flow_time = 5)


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
    wait_until = datetime.now(timezone.utc) + timedelta(hours=1)
    break_loop = False
    while not break_loop:
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
        if wait_until < datetime.now(timezone.utc):
            break_loop = True

def loop_from_button(Button):
    button_is_pressed = Button(12).wait_for_press(timeout=900)
    if button_is_pressed:
        loop_relays()

def flow_calibration(flow_time):
    return flow_time

if __name__ == '__main__':
    while True:
        light = day_or_night(place="brussels")
        if light == 1:
            soil_sensors_thread = threading.Thread(target=loop_from_soil_sensors).start()
            button_thread = threading.Thread(target=loop_from_button, args=(Button, )).start()
            soil_sensors_thread.join()
            button_thread.join()
        else:
            time.sleep(900) 

