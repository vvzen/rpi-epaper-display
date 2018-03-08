import smbus
import time

bus = smbus.SMBus(1)

# this is the address we setup in the arduino
ADDRESS = 0x04

def write_number(value):
    bus.write_byte(ADDRESS, value)
    return -1

def read_number():
    number = bus.read_byte(ADDRESS)
    return number

while True:
    var = input("Enter 1 - 9: ")
    if not var:
        continue

    write_number(var)
    print "Hi, arduino, I sent you: {}".format(var)
    time.sleep(1)

    number = read_number()
    print "Arduino: Hey RPI, I received a digit: {}".format(number)