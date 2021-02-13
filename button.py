from gpiozero import Button

button = Button(button_port)

button.wait_for_press(timeout=300)
