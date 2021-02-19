import time
import subprocess

from gpiozero import Button


def toggle_main_pywatering(main_running):
    if main_running == True:
        cmd = "sudo systemctl stop pywatering.service"
        main_running = False
        print("Process main.py stopped")
    elif main_running == False:
        cmd = "sudo systemctl start pywatering.service"
        main_running = True
        print("Process main.py started")
    subprocess.call([cmd], shell=True)
    return main_running

def stop_button(pin, timeout, main_running):
    while True:
        button_is_pressed = Button(pin).wait_for_press(timeout=timeout)
        if button_is_pressed:
            main_running = toggle_main_pywatering(main_running)


if __name__ == '__main__':
    main_running = True
    timeout = 3600
    stop_button(6, timeout, main_running)