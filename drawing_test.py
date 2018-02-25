#!/usr/bin/python
#*- coding: utf-8 *-
import RPi.GPIO as GPIO
import epd2in9 # waveshare module for the epaper display
import Image, ImageDraw, ImageFont, ImageChops  # PIL - PythonImageLibrary
import time, datetime, sys, signal, urllib, requests, random, os
from StringIO import StringIO
from markov.markovchain import Markov # simple class for generating markov sentences
import button_logic # just for handling button presses
try:
    DEBUG = int(os.getenv("DEBUG"))
except TypeError:
    DEBUG = 0

# global vars
current_dir = os.path.abspath(os.path.dirname(__file__))
# pin vars
trigger_pin = 13
change_state_pin = 6
green_led = 21
blue_led = 16
yellow_led = 20

def generate_sentence(font):
    # generate sentence
    markov = Markov(order=2)
    markov.train(os.path.join(current_dir, "source", "data", "motivational.txt"))
    g_sentence = markov.generate(4)

    # remove all special symbols
    g_sentence = g_sentence.replace("’", "'").replace("\n", " ").replace("”", "")

    # calculates padding so that it fits nicely in the display
    padding_x = (epd2in9.EPD_WIDTH - float(font.getsize(g_sentence)[0])) / 2
    padding_y = (epd2in9.EPD_HEIGHT - float(font.getsize(g_sentence)[1])) / 2

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
    image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 0)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    
    # perform initial setup of display and GPIO
    button_logic.setup_gpio(change_state_pin, trigger_pin, yellow_led, blue_led, green_led)
    # announce that we're ready
    GPIO.output(green_led, True)

    # for partial update
    epd.init(epd.lut_partial_update)

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
            
            # draw.rectangle([0, 0, 10, 10], fill=0)
            text_image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 0)
            d = ImageDraw.Draw(text_image)
            d.text((10, 10), "Example", fill=255, font=andale_ttf_small)
            
            text_image.save("current_text.png")

            combined = ImageChops.add(image, text_image)
            combined.save("current_image.png")

            epd.clear_frame_memory(0xFF)
            epd.set_frame_memory(combined, 0, 0)
            epd.display_frame()

            epd.delay_ms(2000)

            epd.clear_frame_memory(0xFF)
            epd.display_frame()
            epd.clear_frame_memory(0xFF)
            epd.display_frame()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
