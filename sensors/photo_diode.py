import RPi.GPIO as GPIO
import time


def get_light(middle_pin, positive_pin):
    GPIO.setmode(GPIO.BCM)
    cap = 0.000001
    adj = 2.130620985
    resistance = 330  # ohm
    capacitor = 10  # micro faraday
    time_unit = resistance * capacitor / 1000000
    charging_time_without_photo_resistor = 5 * time_unit
    # Charge the capacitor
    GPIO.setup(middle_pin, GPIO.OUT)
    GPIO.setup(positive_pin, GPIO.OUT)
    GPIO.output(middle_pin, False)
    GPIO.output(positive_pin, False)
    time.sleep(charging_time_without_photo_resistor)
    # Discharge the capacitor
    GPIO.setup(middle_pin, GPIO.IN)
    time.sleep(charging_time_without_photo_resistor)
    GPIO.output(positive_pin, True)
    start_time = time.time()
    end_time = time.time()
    while (GPIO.input(middle_pin) == GPIO.LOW):
        end_time = time.time()
    measure_resistance = end_time - start_time
    resistance = (measure_resistance / capacitor) * adj
    return resistance


def normalize_light(resistance):
    min_value = 0.0005
    max_value = 0.15
    normalized_light = 1 - (resistance - min_value) / max_value
    return pow(normalized_light,3)


if __name__ == '__main__':
    resistance = get_light(13, 26)
    normalized_light = normalize_light(resistance)
    print(resistance)
    print(normalized_light)