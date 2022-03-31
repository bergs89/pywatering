import time
import numpy as np

from sensors.libraries import ads1115


def get_sensor_voltage(analog_signal):
    gain = 1
    SCL_pin = 3
    SDA_pin = 2
    voltage = ads1115.get_analog_voltage(SCL_pin, SDA_pin, analog_signal, gain)
    return voltage

def get_moisture(analog_signal):
    voltage = get_sensor_voltage(analog_signal)
    min_v, max_v, threshold = calibration(analog_signal)
    if voltage < threshold and voltage > min_v:
        soil_moisture = 1 #soil is wet
        print("Sensor number: " + str(analog_signal) + " says that the soil is wet.")
    elif voltage > threshold and voltage < max_v:
        soil_moisture = 0 #soil is not wet
        print("Sensor number: " + str(analog_signal) + " says that the soil is dry.")
    elif voltage < threshold and voltage < min_v:
        soil_moisture = 1
        print("Sensor number: " + str(analog_signal) + " might be faulty or disconnected.")
    elif voltage > threshold and voltage > max_v:
        soil_moisture = 1
        print("Sensor number: " + str(analog_signal) + " might be faulty and should be checked soon.")
    else:
        soil_moisture = 1
        print("Something is wrong.")
    return soil_moisture

def calibration(analog_signal):
    if analog_signal == 0:
        min_v = 1.32
        max_v = 2.87
        threshold = np.mean([min_v, max_v])
    elif analog_signal == 1:
        min_v = 1.32
        max_v = 2.9
        threshold = np.mean([min_v, max_v])
    elif analog_signal == 2:
        min_v = 1.36
        max_v = 2.95
        threshold = np.mean([min_v, max_v])
    elif analog_signal == 3:
        min_v = 1.35
        max_v = 2.93
        threshold = np.mean([min_v, max_v])
    return min_v, max_v, threshold

if __name__ == "__main__":
    while True:
        for analog_signal in range(4):
            moisture = get_moisture(analog_signal)
            print("Moisture on pin: " + str(analog_signal) + " is: " +str(moisture))
        time.sleep(1)
