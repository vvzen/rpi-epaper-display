import RPI.GPIO as GPIO
import time

change_state_btn_pin = 27

# setup gpio
GPIO.setMode(GPIO.BCM)
GPIO.setup(change_state_btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    button_state = GPIO.input(change_state_btn_pin)

    if button_state:
        print "Button pressed"
        time.sleep(0.2)