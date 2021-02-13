import RPi.GPIO as GPIO
import time


def get_light(middle_pin, positive_pin):
    i = 0
    while i < 2:
        GPIO.setmode(GPIO.BCM)
        constant = 18
        resistance = 330  # ohm
        capacitor = 10  # micro faraday
        time_unit = resistance * capacitor / 1000000
        charging_time_without_photo_resistor = 3 * time_unit
        # Charge the capacitor
        GPIO.setup(middle_pin, GPIO.OUT)
        GPIO.setup(positive_pin, GPIO.OUT)
        GPIO.output(middle_pin, False)
        GPIO.output(positive_pin, False)
        time.sleep(0.25)
        # Discharge the capacitor
        GPIO.setup(middle_pin, GPIO.IN)
        time.sleep(0.25)
        GPIO.output(positive_pin, True)
        start_time = time.time()
        end_time = time.time()
        timeout = 0
        while (GPIO.input(middle_pin) == GPIO.LOW) and timeout < 0.5555:
            end_time = time.time()
            timeout = end_time - start_time
        measure_resistance = end_time - start_time
        resistance_estimation = (measure_resistance / capacitor * 1000000) * constant
        i = i + 1
    return resistance_estimation


def normalize_light(resistance):
    min_value = 0
    max_value = 1000000
    normalized_light = 1 - (resistance - min_value) / max_value
    return pow(normalized_light,1)


if __name__ == '__main__':
    while True:
        resistance_est = get_light(13, 26)
        normalized_light = normalize_light(resistance_est)
	print(normalized_light)
	print(resistance_est)
	time.sleep(0.5)
