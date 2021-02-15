import time

from libraries import ads1115


def get_moisture(analog_signal):
    gain = 1
    SCL_pin = 1
    SDA_pin = 0
    voltage = ads1115.get_analog_voltage(SCL_pin, SDA_pin, analog_signal, gain)
    if voltage > 1.5:
        soil_moisture = 1
    else:
        soil_moisture = 0
    print(soil_moisture)
    return soil_moisture


if __name__ == "__main__":
    while True:
        for analog_signal in range(4):
            moisture = get_moisture(analog_signal)
            print("Moisture on pin: " + str(analog_signal) + " is: " +str(moisture))
        time.sleep(1)