import smbus
import time

bus = smbus.SMBus(1)

# this is the address we setup in the arduino
ADDRESS = 0x04

def write_number(value):
    bus.write_byte(ADDRESS, value)
    return -1

def write_string(value):
    for c in str(value):
        print c
        bus.write_byte(ADDRESS, ord(c)) # send ASCII encoding
    return -1

def read_number():
    number = bus.read_byte(ADDRESS)
    return number

# def read_string():
#     number = bus.read_byte(ADDRESS)
#     return number

def main():
    b = 0
    while True:
        var = input("Enter 1 - 9: ")
        if b == 0:
            # var = "These aren't the droids you're looking for"
            write_number(var)
            # write_string(var)
            print "Hi, arduino, I sent you: {}".format(var)
            b += 1
            time.sleep(1)
        number = read_number()
        print "Arduino: Hey RPI, I received a digit: {}".format(number)
try:
    main()
except KeyboardInterrupt:
    pass
