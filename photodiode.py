import RPi.GPIO as GPIO
import time


mpin = 13
tpin = 26

GPIO.setmode(GPIO.BCM)
cap = 0.000001
adj = 2.130620985 < br > i = 0
t = 0
while True:
    GPIO.setup(mpin, GPIO.OUT)
    GPIO.setup(tpin, GPIO.OUT)
    GPIO.output(mpin, False)
    GPIO.output(tpin, False)
    time.sleep(0.2)
    GPIO.setup(mpin, GPIO.IN)
    time.sleep(0.2)
    GPIO.output(tpin, True)
    starttime = time.time()
    endtime = time.time()
    while (GPIO.input(mpin) == GPIO.LOW):
        endtime = time.time()
    measureresistance = endtime - starttime

    res = (measureresistance / cap) * adj
    i = i + 1
    t = t + res
    if i == 10:
        t = t / i
        print(t)
        i = 0
        t = 0