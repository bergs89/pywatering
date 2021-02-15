from libraries import ads1115bergs


def get_moisture(port):
    gain = 1
    SCL_pin = 1
    SDA_pin = 0
    for a in range(4):
        voltage = ads1115bergs.get_analog_voltage(SCL_pin, SDA_pin, a, gain)
        if voltage > 1.5:
            print("moist")
        else:
            print(dry)
    return

