import RPi.GPIO as GPIO
import time

# pin vars
trigger_pin = 13
change_state_pin = 6
green_led = 21
blue_led = 16
yellow_led = 20


# app logic vars
COOKIE = 0
MOTIVATIONAL = 1
MARKOV = 2
app_mode = COOKIE

# setup gpio
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(change_state_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

GPIO.output(yellow_led, False)
GPIO.output(green_led, False)
GPIO.output(blue_led, False)


def change_state():
    
    global app_mode
    app_mode += 1
    if app_mode > 2:
	app_mode = 0

    if app_mode == COOKIE:
	GPIO.output(blue_led, False)
        GPIO.output(green_led, False)
        GPIO.output(yellow_led, True)
    elif app_mode == MOTIVATIONAL:
	GPIO.output(blue_led, True)
        GPIO.output(green_led, False)
        GPIO.output(yellow_led, False)	
    elif app_mode == MARKOV:
	GPIO.output(blue_led, False)
        GPIO.output(green_led, True)
        GPIO.output(yellow_led, False) 

    print "Button pressed, app mode: {}".format(app_mode)
    
    time.sleep(0.5)

#GPIO.add_event_detect(change_state_btn_pin, GPIO.FALLING, callback=button_callback, bouncetime=50)


while True:
    
    button_state = GPIO.input(change_state_pin)

    if button_state == False:
        change_state()
