# -*- coding: utf-8 -*- 
import os
import random
import requests
from bs4 import BeautifulSoup

current_dir = os.path.abspath(os.path.dirname(__file__))

''' # create motivational dataset
with open(os.path.join(current_dir, "source", "data", "motivational_quotes.txt"), "r") as f:
    motivational = [line.replace("”", "'").replace("‘", "'").replace("…", "...") for line in f.read().split("\n") if len(line) < 29]
    # print random.sample(motivational, 1)
    print "\n".join(motivational) '''

cookies_counter = 0

while cookies_counter < 50:
    html_doc = requests.get("http://www.fortunecookiemessage.com/").text
    soup = BeautifulSoup(html_doc, "html.parser")

    links = [link.text for link in soup.find_all("a") if link.get("class") is not None]
    cookie_message = links[1]

    if len(cookie_message) < 29:
        print "adding {} to cookies".format(links[1])
        with open(os.path.join(current_dir, "source", "data", "fortune_cookies.txt"), "a") as cf:
            cf.write("\n{}".format(links[1]))
        cookies_counter+=1

# target_link =  [l.get_text() for l in links if l.get("class") == "cookie-link"]
# print target_link

# create fortune cookies dataset
''' with open(os.path.join(current_dir, "source", "data", "RAW_fortune_cookies.txt"), "r") as f:
    cookies = [line.replace("”", "'").replace("‘", "'").replace("…", "...") for line in f.read().split("\n") if len(line) < 29]
    # print random.sample(motivational, 1)
    print "\n".join(cookies)
 '''