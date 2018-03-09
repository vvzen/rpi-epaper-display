#!/usr/bin/python
#*- coding: utf-8 *-
import RPi.GPIO as GPIO
import smbus
import os, time, random
import button_logic # just for handling button presses
from markov.markovchain import Markov # simple class for generating markov sentences

bus = smbus.SMBus(1)

# global variables
ADDRESS = 0x04 # this is the slave address we setup in the arduino
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
# pin vars
trigger_pin = 13
change_state_pin = 6
green_led = 21
blue_led = 16
yellow_led = 20

def write_number(value):
    bus.write_byte(ADDRESS, value)
    return -1

def write_string(value):
    # as first byte, send the total length of the string
    print "length of string: {}".format(len(str(value)))
    bus.write_byte(ADDRESS, len(str(value)))
    # then send each char in the string
    for char in str(value):
        bus.write_byte(ADDRESS, ord(char)) # send ASCII encoding
    return -1

def read_number():
    number = bus.read_byte(ADDRESS)
    return number

def pick_random_sentence(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return random.choice(lines)

def generate_sentence(mode):
    '''
    generate the required sentence (markov, cookie, etc..)
    and returns the pos_x and y after calculating the length of the phrase
    in order to draw it centered to the display
    '''

    # generate sentence
    markov = Markov(order=2)

    if mode == button_logic.MARKOV:
        markov.train(os.path.join(CURRENT_DIR, "source", "data", "motivational_markov.txt"))
        g_sentence = markov.generate(4)
        # check if sentence is too long
        while len(g_sentence) > 34:
            g_sentence = markov.generate(4)
    elif mode == button_logic.QUOTE:
        #markov.train(os.path.join(CURRENT_DIR, "source", "data", "star_wars_quotes.txt"))
        g_sentence = pick_random_sentence(os.path.join(CURRENT_DIR, "source", "data", "star_wars_quotes.txt"))
        while len(g_sentence) > 34:
            g_sentence = pick_random_sentence(os.path.join(CURRENT_DIR, "source", "data", "star_wars_quotes.txt"))
    elif mode == button_logic.COOKIE:
        #markov.train(os.path.join(CURRENT_DIR, "source", "data", "fortune_cookies.txt"))
        g_sentence = pick_random_sentence(os.path.join(CURRENT_DIR, "source", "data", "fortune_cookies.txt"))
        while len(g_sentence) > 34:
            g_sentence = pick_random_sentence(os.path.join(CURRENT_DIR, "source", "data", "star_wars_quotes.txt"))

    # remove all special symbols
    g_sentence = g_sentence.replace("’", "'").replace("\n", " ").replace("”", "").replace("$", "")
    #g_sentence = g_sentence.replace(" ", r"\n")

    print "----> {}".format(g_sentence)

    return g_sentence

def main():

    # wait for the arduino to be ready
    time.sleep(10)

    print "rpi ready"

    # perform initial setup of display and GPIO
    button_logic.setup_gpio(change_state_pin, trigger_pin, yellow_led, blue_led, green_led)

    # announce that we're ready
    GPIO.output(green_led, True)

    # b = 0
    while True:

        state_button = GPIO.input(change_state_pin)
        trigger_button = GPIO.input(trigger_pin)

        if state_button == False:
            button_logic.change_state(yellow_led, blue_led, green_led)
            print "Button press!"
            time.sleep(0.2)

        elif trigger_button == False:
            sentence = generate_sentence(button_logic.app_mode)
            write_string(sentence)
            print "Hi, arduino, I sent you: {}".format(sentence)
            time.sleep(1)
        
        ''' # var = input("Enter 1 - 9: ")
        if b == 0:
            var = "These aren't the droids you're looking for"
            # write_number(var)
            write_string(var)
            print "Hi, arduino, I sent you: {}".format(var)
            b += 1
            time.sleep(1) '''

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        #pwm.stop()
        GPIO.cleanup()