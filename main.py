from sensors import humidity_sensor, relay

from time import time
from gpiozero import Button


button = Button(button_port)


while True:
    ports = [(1,1), (2,2), (3,3), (4,4)]
    for port in ports:
        relay_port, sensor_port = port
        if humidity_sensor.get_humidity(sensor_port) < 0.1:
            relay.activate_relay(relay_port)
            time.sleep(1)
    button.wait_for_press(timeout=300)
    relay.activate_relays_in_sequence(relay_ports)