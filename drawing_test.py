#!/usr/bin/python
#*- coding: utf-8 *-
import RPi.GPIO as GPIO
import epd2in9 # waveshare module for the epaper display
import Image, ImageDraw, ImageFont, ImageChops  # PIL - PythonImageLibrary
import time, datetime, sys, signal, urllib, requests, random, os
from StringIO import StringIO
from markov.markovchain import Markov # simple class for generating markov sentences
import button_logic # just for handling button presses
import default
try:
    DEBUG = int(os.getenv("DEBUG"))
except TypeError:
    DEBUG = 0

# global vars
current_dir = os.path.abspath(os.path.dirname(__file__))
pwn = None

# pin vars
servo_pin = 4 # physical 7
trigger_pin = 13
change_state_pin = 6
green_led = 21
blue_led = 16
yellow_led = 20

def remap(x, in_min, in_max, out_min, out_max):
    '''
    remaps x value from one range to the other one
    '''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup_servo():
    '''
    setup pwn for servo
    '''
    GPIO.setup(servo_pin, GPIO.OUT)
    global pwn
    pwm = GPIO.PWM(servo_pin, 50) # pin, duty cycle frequency
    pwm.start(7.5) # make servo go into neutral position

def move_servo(angle):
    '''
    rotate the servo to the given angle
    '''

    # constrain angle to min and max values
    if angle > 90:
        angle = 90
    if angle < -90:
        angle = -90
    
    percentage = remap(angle, -90, 90, 2.5, 12.5)
    GPIO.output(servo_pin, True)
    pwn.ChangeDutyCycle(percentage)
    time.sleep(1)
    GPIO.output(servo_pin, False)

def generate_sentence(font):
    '''
    generate the required sentence (markov, cookie, etc..)
    and returns the pos_x and y after calculating the length of the phrase
    in order to draw it centered to the display
    '''

    # generate sentence
    markov = Markov(order=2)
    markov.train(os.path.join(current_dir, "source", "data", "motivational_markov.txt"))
    g_sentence = markov.generate(4)

    print "here"
    # test if sentence is too long
    while len(g_sentence) > 29:
	g_sentence = markov.generate(4)

    # remove all special symbols
    g_sentence = g_sentence.replace("’", "'").replace("\n", " ").replace("”", "")
    #g_sentence = g_sentence.replace(" ", r"\n")

    # calculates padding so that it fits nicely in the display
    padding_x = (epd2in9.EPD_HEIGHT - float(font.getsize(g_sentence)[0])) * 0.5
    padding_y = (epd2in9.EPD_WIDTH - float(font.getsize(g_sentence)[1])) * 0.5

    print "----> {}".format(g_sentence)

    if DEBUG:
        print "length of sentence: {}".format(len(g_sentence))
    	print "pixel size of sentence: {}".format(andale_ttf_small.getsize(g_sentence))

    return g_sentence, padding_x, padding_y

# our entry point
def main():

    # main_img is used as screen buffer, all image composing/drawing is done in PIL,
    # the main_img is then copied to the display (drawing on the disp itself is no fun)
    # main_img = Image.new("1", (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT))
    # draw = ImageDraw.Draw(main_img)

    # fonts for drawing within PIL
    andale_ttf_small = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 16)
    andale_ttf_large = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 26)

    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    
    # perform initial setup of display and GPIO
    button_logic.setup_gpio(change_state_pin, trigger_pin, yellow_led, blue_led, green_led)

    # perform initial setup of the servo
    setup_servo()
    move_servo(0)
    move_servo(180)
    move_servo(90)
    
    # announce that we're ready
    GPIO.output(green_led, True)

    # FIXME: draw to epaper display
    default.main()

    while True:
        starttime = time.time()

        state_button = GPIO.input(change_state_pin)
        trigger_button = GPIO.input(trigger_pin)

        if state_button == False:
            button_logic.change_state(yellow_led, blue_led, green_led)
            print "Button press!"
            time.sleep(0.2)

        elif trigger_button == False:
            text, pos_x, pos_y = generate_sentence(font=andale_ttf_small)

            # create binary image filled with white
            base_image = Image.new("1", size=(epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), color=255)

            # create the text image
            text_image = Image.new('1', (epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH))
            # draw the text and rotate it -90 degrees so that it fits the portait orientation
            text_draw_buffer = ImageDraw.Draw(text_image)
            text_draw_buffer.text((pos_x, pos_y), text,  font=andale_ttf_small, fill=255)
            text_image = text_image.rotate(270,  expand=1)

            result = ImageChops.multiply(text_image, base_image)
	    result.save("result.png")

            epd.clear_frame_memory(0xFF)
            epd.set_frame_memory(result, 0, 0)
            epd.display_frame()

            epd.delay_ms(2000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        #pwm.stop()
        GPIO.cleanup()
