import sys
import time
import threading

from gpiozero import Button
from sensors import relay, soil_moisture
from libs.light import day_or_night
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client


def on_connect_st(
        client,
        userdata,
        flags,
        rc,
):
    print("Connected")
    client.subscribe("PYWATERING")


def on_connect_plant1(
        client,
        userdata,
        flags,
        rc,
):
    print("Connected")
    client.subscribe("PLANT1")


def on_connect_plant2(
        client,
        userdata,
        flags,
        rc,
):
    print("Connected")
    client.subscribe("PLANT2")

def on_connect_plant3(
        client,
        userdata,
        flags,
        rc,
):
    print("Connected")
    client.subscribe("PLANT3")


def on_connect_plant4(
        client,
        userdata,
        flags,
        rc,
):
    print("Connected")
    client.subscribe("PLANT4")


def on_message(
        client,
        userdata,
        msg,
):
    m_decode = str(msg.payload.decode("utf-8"))
    print("Received message from MQTT: " + m_decode + " from topic: " + msg.topic)
    global global_message
    global_message = m_decode


def get_mqtt_payload(topic):
    mqttBroker = "localhost"
    client = Client("Temperature_Inside")

    if topic == "PYWATERING":
        client.on_connect = on_connect_st
    elif topic == "PLANT1":
        client.on_connect = on_connect_plant1
    elif topic == "PLANT2":
        client.on_connect = on_connect_plant2
    elif topic == "PLANT3":
        client.on_connect = on_connect_plant3
    elif topic == "PLANT4":
        client.on_connect = on_connect_plant4

    client.on_message = on_message
    client.connect("localhost")
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
    return global_message


# def read_pywatering_toogle_mqtt(
#         topic,
# ):
#     mqttBroker = "localhost"
#     client = mqtt.Client("Temperature_Inside")
#     client.connect(mqttBroker)
#     result, mid = client.subscribe(
#         topic,
#     )
#     return mid


def publish_soil_status_mqtt(
        analog_signal,
        soil_wet,
):
    mqttBroker = "localhost"
    client = mqtt.Client("Temperature_Inside")
    client.connect(mqttBroker)
    moisture_sensor_number = analog_signal + 1
    moisture_sensor_name = "MOISTURE" + str(moisture_sensor_number)
    if soil_wet == 1:
        payload = "WET SOIL"
    elif soil_wet == 0:
        payload = "DRY SOIL"
    client.publish(moisture_sensor_name, payload)
    print("Published MQTT " + moisture_sensor_name+ ": " + payload)


def set_relays_off():
    relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        relay.set_relay(False, relay.relay(relay_channel))


def loop_relays(
    plant1_toggle,
    plant2_toggle,
    plant3_toggle,
    plant4_toggle,
    flow_time,
):
    relay_channels = []
    if plant1_toggle == 1:
        relay_channels.append(4)
    if plant2_toggle == 1:
        relay_channels.append(27)
    if plant3_toggle == 1:
        relay_channels.append(22)
    if plant4_toggle == 1:
        relay_channels.append(23)
    # relay_channels = [4, 27, 22, 23]
    for relay_channel in relay_channels:
        pump_water(
            relay_channel,
            flow_time
        )


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


def loop_from_soil_sensors(
        plant1_toggle,
        plant2_toggle,
        plant3_toggle,
        plant4_toggle,
        flow_time,
):
    relay_channels = [4, 27, 22, 23]
    toggles = [
        plant1_toggle,
        plant2_toggle,
        plant3_toggle,
        plant4_toggle,
    ]
    for analog_signal in range(0,4):
        soil_wet = soil_moisture.get_moisture(analog_signal)
        publish_soil_status_mqtt(
            analog_signal,
            soil_wet,
        )
        if soil_wet == 0 and toggles[analog_signal] == 1:
            time.sleep(1)
            pump_water(
                relay_channels[analog_signal],
                flow_time,
            )
            time.sleep(1)


def flow_button(
        pin,
        plant1_toggle,
        plant2_toggle,
        plant3_toggle,
        plant4_toggle,
        timeout,
):
    start_time = time.time()
    total_time = 0
    while total_time < timeout:
        button_is_pressed = Button(pin).wait_for_press(timeout=timeout)
        if button_is_pressed:
            loop_relays(
                plant1_toggle,
                plant2_toggle,
                plant3_toggle,
                plant4_toggle,
                flow_time,
                        )
        total_time = time.time() - start_time


def flow_calibration(flow_time):
    return flow_time


if __name__ == '__main__':
    debugging = 0
    timeout = 10
    flow_time = 2
    set_relays_off()
    # while True:
    thread_list = []
    light = day_or_night(place="brussels")

    system_toggle = get_mqtt_payload("PYWATERING",)
    plant1_toggle = get_mqtt_payload("PLANT1",)
    plant2_toggle = get_mqtt_payload("PLANT2",)
    plant3_toggle = get_mqtt_payload("PLANT3")
    plant4_toggle = get_mqtt_payload("PLANT4",)

    if (light == 1 and system_toggle == 1) or debugging == 1:
        soil_sensors_thread = threading.Thread(
            target=loop_from_soil_sensors,
            args=(
                plant1_toggle,
                plant2_toggle,
                plant3_toggle,
                plant4_toggle,
                flow_time,
            ),
            daemon=True,
        )
        thread_list.append(soil_sensors_thread)
        # flow_button = threading.Thread(
        #     target=flow_button,
        #     args=(
        #         12,
        #         plant1_toggle,
        #         plant2_toggle,
        #         plant3_toggle,
        #         plant4_toggle,
        #         timeout,
        #     ),
        #     daemon=True,
        # )

        # thread_list.append(flow_button)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

