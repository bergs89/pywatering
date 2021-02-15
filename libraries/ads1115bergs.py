import time
# import board
import busio
import numpy as np

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def get_analog_voltage(SCL_pin, SDA_pin, a, gain):
    # Create the I2C bus
    # i2c = busio.I2C(board.SCL, board.SDA)
    i2c = busio.I2C(SCL_pin, SDA_pin)
    # Create the ADS object
    # ads = ADS.ADS1015(i2c)
    ads = ADS.ADS1115(i2c)
    # Create a sinlge ended channel on Pin 0
    #   Max counts for ADS1015 = 2047
    #                  ADS1115 = 32767
    if a == 0:
        chan = AnalogIn(ads, ADS.P0)
    elif a == 1:
        chan = AnalogIn(ads, ADS.P1)
    elif a == 2:
        chan = AnalogIn(ads, ADS.P2)
    elif a == 3:
        chan = AnalogIn(ads, ADS.P3)
    else:
        raise IndexError
    # The ADS1015 and ADS1115 both have the same gain options.
    #
    #       GAIN    RANGE (V)
    #       ----    ---------
    #        2/3    +/- 6.144
    #          1    +/- 4.096
    #          2    +/- 2.048
    #          4    +/- 1.024
    #          8    +/- 0.512
    #         16    +/- 0.256
    #
    # gains = (2 / 3, 1, 2, 4, 8, 16)
    ads.gain = gain
    return chan.voltage


def get_analog_voltage_continuous(SCL_pin, SDA_pin, a, gain, timeout):
    start_time = time.time()
    voltages = []
    runtime = 0
    while timeout > runtime:
        this_voltage = get_analog_voltage(SCL_pin, SDA_pin, a, gain)
        voltages.append(this_voltage)
        runtime = time.time() - start_time
    runtime_array = np.array(voltages)
    return runtime_array.mean(), runtime_array



