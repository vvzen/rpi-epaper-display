import RPi.GPIO as GPIO

# app logic vars
COOKIE = 0
MOTIVATIONAL = 1
MARKOV = 2
app_mode = COOKIE

# setup gpio
# @args:
#   change state and trigger buttons
#   yellow, blue and green leds
def setup_gpio(cs_btn, tr_btn, y_led, b_led, g_led):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cs_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(tr_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(y, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)

    GPIO.output(y_led, False)
    GPIO.output(g_led, False)
    GPIO.output(b_led, False)

# on button press change current state
def change_state(y_led, b_led, g_led):
    
    global app_mode
    app_mode += 1
    if app_mode > 2:
        app_mode = 0

    if app_mode == COOKIE:
        GPIO.output(b_led, False)
        GPIO.output(g_led, False)
        GPIO.output(y_led, True)
    elif app_mode == MOTIVATIONAL:
        GPIO.output(b_led, True)
        GPIO.output(g_led, False)
        GPIO.output(y_led, False)	
    elif app_mode == MARKOV:
        GPIO.output(b_led, False)
        GPIO.output(g_led, True)
        GPIO.output(y_led, False) 

    print "Button pressed, app mode: {}".format(app_mode)
