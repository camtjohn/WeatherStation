import wiringpi as wiringpi
import sys
import time


# Setup i2c module wiringpi
pin_base = 65
i2c_addr = 0x20
wiringpi.wiringPiSetup()
wiringpi.pcf8574Setup(pin_base, i2c_addr)

pin_base2 = 73
i2c_addr2 = 0x21
wiringpi.pcf8574Setup(pin_base2, i2c_addr2)


# Base pin is 65, this function allows to input 0-7 to define pin
def pin_mod(pin):
	pin_mod = pin+65
	return pin_mod

# pull i2c pins 1-8 high
for pin in range(1,13):
    wiringpi.digitalWrite(pin_mod(pin),1)
	
led1 = pin_mod(0) # pin0 on i2c expander(pcf8574)
led2 = pin_mod(1)
led3 = pin_mod(2)
led4 = pin_mod(3)
led5 = pin_mod(4)
led6 = pin_mod(5)
led7 = pin_mod(6)
led8 = pin_mod(7)
led9 = pin_mod(8)
led10 = pin_mod(9)

list_led = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]

led_on = 0	# Led connected to high, drive low to turn on)
led_off = 1	# drive high to turn off

def on(led):
    wiringpi.digitalWrite(led, led_on)
    
def off(led):
    wiringpi.digitalWrite(led, led_off)

def blink(led):
    on(led)
    time.sleep(0.2)
    off(led)

def blink_all():
    t = 0.1
    
    for led in list_led: on(led); time.sleep(t)
    for led in list_led: off(led); time.sleep(t)


def off_all():
    for led in list_led: off(led)

def on_all():
    for led in list_led: on(led)

blink_all()
