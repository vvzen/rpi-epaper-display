#!/usr/bin/python
#*- coding: utf-8 *-
import RPi.GPIO as GPIO
import epd2in9 # waveshare module for the epaper display
import Image, ImageDraw, ImageFont  # PIL - PythonImageLibrary
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

# fonts for drawing within PIL
andale_ttf_small = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 16)
andale_ttf_large = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 26)

# main_img is used as screen buffer, all image composing/drawing is done in PIL,
# the main_img is then copied to the display (drawing on the disp itself is no fun)
main_img = Image.new("1", (DISPLAY_WIDTH, DISPLAY_HEIGHT))
draw = ImageDraw.Draw(main_img)

def generate_sentence(font):
    # generate sentence
    markov = Markov(order=2)
    markov.train(os.path.join(current_dir, "source", "data", "motivational.txt"))
    g_sentence = markov.generate(4)

    # remove all special symbols
    g_sentence = g_sentence.replace("’", "'").replace("\n", " ").replace("”", "")

    # calculates padding so that it fits nicely in the display
    padding_x = (DISPLAY_WIDTH - float(font.getsize(g_sentence)[0])) / 2
    padding_y = (DISPLAY_HEIGHT - float(font.getsize(g_sentence)[1])) / 2

    print "----> {}".format(g_sentence)

    if DEBUG:
        print "length of sentence: {}".format(len(g_sentence))
    	print "pixel size of sentence: {}".format(andale_ttf_small.getsize(g_sentence))

    return g_sentence, padding_x, padding_y

# our entry point
def main():

    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in9.EPD_WIDTH, epd2in9.EPD_HEIGHT), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    
    # perform initial setup of display and GPIO
    button_logic.setup_gpio(change_state_pin, trigger_pin, yellow_led, blue_led, green_led)
    # announce that we're ready
    GPIO.output(green_led, True)

    draw.rectangle([0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT], fill="black")
    image_to_display(main_img)
    time.sleep(1)

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
            
            # from waveshare demo
            draw.text((8, 12), 'Hello world!', font=andale_ttf_small, fill = 255)
            draw.text((8, 36), 'e-Paper Demo', font=andale_ttf_small, fill = 0)
            draw.line((16, 60, 56, 60), fill = 0)
            draw.line((56, 60, 56, 110), fill = 0)
            draw.line((16, 110, 56, 110), fill = 0)
            draw.line((16, 110, 16, 60), fill = 0)
            draw.line((16, 60, 56, 110), fill = 0)
            draw.line((56, 60, 16, 110), fill = 0)
            
            # draw.rectangle([0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT], fill=255)
            # draw.text((pos_x, pos_y), text, fill=0, font=andale_ttf_small)

            # clear memory
            epd.clear_frame_memory(0xFF)
            epd.set_frame_memory(image, 0, 0)
            epd.display_frame()

            epd.delay_ms(2000)

            # # draw a rectangle to clear the image
            # draw.rectangle((0, 0, image_width, image_height), fill = 255)
            # draw.text((0, 0), time.strftime('%M:%S'), font = font, fill = 0)
            # epd.set_frame_memory(time_image.rotate(270), 80, 80)
            # epd.display_frame()
            
            # main_img.save("current_image.png")
            # print "updating display.."
            # image_to_display(main_img)
	    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
