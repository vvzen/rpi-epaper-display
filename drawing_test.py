#!/usr/bin/python
#*- coding: utf-8 *-
import Image, ImageDraw, ImageFont  # PIL - PythonImageLibrary
import time, datetime, sys, signal, urllib, requests, random, os
from StringIO import StringIO
from markov.markovchain import Markov # simple class for generating markov sentences
DEBUG = os.getenv("DEBUG")
if not DEBUG:
    import spidev as SPI # serial peripheral interface bus, where the display connects
    from EPD_driver import EPD_driver

# global vars
DISPLAY_WIDTH = 296
DISPLAY_HEIGHT = 128
current_dir = os.path.abspath(os.path.dirname(__file__))

# quit app gracefully
def sigterm_handler(signum, frame):
    print 'closing app, SIGTERM signal received'
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)
random.seed(time.time())

# writes the image to the display
def image_to_display(img):
    # prepare for display
    im = main_img.transpose(Image.ROTATE_90)
    listim = list(im.getdata())
    # print im.format, im.size, im.mode, len(listim)
    # convert to list / bitmap
    listim2 = []
    for y in range(0, im.size[1]):
        for x in range(0, im.size[0]/8):
            val = 0
            for x8 in range(0, 8):
                if listim[(im.size[1]-y-1)*im.size[0] + x*8 + (7-x8)] > 128:
                    # print x,y,x8,'ON'
                    val = val | 0x01 << x8
                else:
                    # print x,y,x8,'OFF'
                    pass
            # print val
            listim2.append(val)
    for x in range(0,1000):
        listim2.append(0)
    # print len(listim2)
    ypos = 0
    xpos = 0
    disp.EPD_Dis_Part(xpos, xpos+im.size[0]-1, ypos, ypos+im.size[1]-1, listim2) # xStart, xEnd, yStart, yEnd, DisBuffer
    uploadtime = time.time()

# initialise the display and clear it
if not DEBUG:
    bus = 0
    device = 0
    disp = EPD_driver(spi = SPI.SpiDev(bus, device))
    print "disp size : %dx%d"%(disp.xDot, disp.yDot)

    print '------------init and Clear full screen------------'
    disp.Dis_Clear_full()
    disp.delay()

    # display part
    disp.EPD_init_Part()
    disp.delay()

# fonts for drawing within PIL
andale_ttf_small = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 15)
andale_ttf_large = ImageFont.truetype("source/fonts/andale_mono/AndaleMono.ttf", 26)

# main_img is used as screen buffer, all image composing/drawing is done in PIL,
# the main_img is then copied to the display (drawing on the disp itself is no fun)
main_img = Image.new("1", (DISPLAY_WIDTH, DISPLAY_HEIGHT))
draw = ImageDraw.Draw(main_img)

# generate sentence
markov = Markov(order=2)
markov.train(os.path.join(current_dir, "source", "data", "motivational.txt"))
sentence = markov.generate(4)

# remove all special symbols
sentence = sentence.replace("’", "'").replace("\n", " ").replace("”", "")

# format sentence so that it fits into the display
padding = (DISPLAY_WIDTH - float(andale_ttf_small.getsize(sentence)[0])) / 2
if DEBUG:
    print "---> {}".format(sentence)
    print "length of sentence: {}".format(len(sentence))
    print "pixel size of sentence: {}".format(andale_ttf_small.getsize(sentence))
    print "display width - sentence size: {}".format(padding)

# our entry point
def main():

    while True:
        starttime = time.time()

        # 
        pos_x = padding
        pos_y = 44
        text = sentence
        draw.text((pos_x, pos_y), sentence, fill=255, font=andale_ttf_small)
        # draw.text((tpx, tpy), text, fill=255, font=andale_ttf_small)

        if DEBUG:
            main_img.save("drawing_test.png")
            break
        else:
            image_to_display(main_img)

        time.sleep(0.3)

if __name__ == "__main__":
    main()