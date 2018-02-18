# rpi-epaper-display README

This little repo contains a little project used for working with a **Waveshare 2.9 E-Paper Display** and a **Raspberry Pi Zero**. It should be taken just as a starting point for your own personal projects!

I recommend also following this guide:
[http://www.instructables.com/id/Waveshare-EPaper-and-a-RaspberryPi/](http://www.instructables.com/id/Waveshare-EPaper-and-a-RaspberryPi/)

I used the following display: [https://www.amazon.co.uk/gp/product/B071JFRV2S/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1](https://www.amazon.co.uk/gp/product/B071JFRV2S/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1)

The pinout used is this:

| e-Paper | Raspberry Pi |
|:-----------|:-----------:|
| 3.3V       | 3.3V (pin1) |
| GND        |GND  (pin6)  |
| DIN        |MOSI (pin19) |   
| CLK        |SCLK (pin23) | 
| CS         |CE0  (pin24) |
| DC         |BCM25(pin22) |
| RST        |BCM17(pin11) |
| BUSY       |BCM24(pin18) |

# For myself
1. When testing on my machine, I use the appropriate venv `source paper-display-venv/bin/activate` and set the env var `DEBUG` to 1

# For everyone
1. When testing on your local machine (if you want to), use the `requirements.txt` file in order to install the required modules.<br>Also set env var DEBUG to 1, like this: `DEBUG=1 python drawing_test.py`
	
	Setting DEBUG to 1 avoids loading modules that you don't have on your local machine and will also create an output image (drawing_test.png) instead of rendering the images on the epaper display. This could be useful to do most of the programming on your machine before sending the code to the raspberry pi.
	
	When you will be working on your raspberry pi you'll need to install these modules:
    `sudo apt-get install python-requests python-pil python-rpi.gpio`

2. SPI must be enabled on the Raspberry-Pi: in /boot/config.txt look for "dtparam=spi=on"
