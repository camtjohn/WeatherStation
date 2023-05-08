#!/usr/bin/python3
import sys
import time
import threading
import RPi.GPIO as GPIO
import weather_module, router_module



# Button press pipes through following filter. Directs the callback to
# diffrent functions based on the current window mode.

def callBtn1(ev=None):
    router_module.button_pressed(1)
def callBtn2(ev=None):
    router_module.button_pressed(2)
def callBtn3(ev=None):
    router_module.button_pressed(3)
def callBtn4(ev=None):
    router_module.button_pressed(4)
def callBtn5(ev=None):
    router_module.button_pressed(5)
def callBtn6(ev=None):
    router_module.button_pressed(6)
def callBtn7(ev=None):
    router_module.button_pressed(7)
def callBtn8(ev=None):
    router_module.button_pressed(8)
def callBtn9(ev=None):
    router_module.button_pressed(9)
def callBtn10(ev=None):
    router_module.button_pressed(10)


# setup buttons button press
def setup():
    # ioConfiguration GPIO assignments
    BtnPin1 = 4
    BtnPin2 = 17
    BtnPin3 = 27
    BtnPin4 = 5
    BtnPin5 = 6

    BtnPin6 = 13
    BtnPin7 = 26
    BtnPin8 = 12
    BtnPin9 = 16
    BtnPin10 = 20
    
    GPIO.setmode(GPIO.BCM) #Use GPIOnumber (not 1-40)
    GPIO.setup(BtnPin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Btnpin mod is input, pulled up to 3.3v
    GPIO.setup(BtnPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BtnPin10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # wait for falling, set bouncetime to prevent callback calling multiple times when btn pressed
    bounce = 300
    GPIO.add_event_detect(BtnPin1, GPIO.FALLING, callback=callBtn1, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=callBtn2, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin3, GPIO.FALLING, callback=callBtn3, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin4, GPIO.FALLING, callback=callBtn4, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin5, GPIO.FALLING, callback=callBtn5, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin6, GPIO.FALLING, callback=callBtn6, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin7, GPIO.FALLING, callback=callBtn7, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin8, GPIO.FALLING, callback=callBtn8, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin9, GPIO.FALLING, callback=callBtn9, bouncetime = bounce)
    GPIO.add_event_detect(BtnPin10, GPIO.FALLING, callback=callBtn10, bouncetime = bounce)




def main():
    print('start')
    time.sleep(3600)


# start program!
if __name__== '__main__':
    setup()
    weather_module.start_timer()
    main()
    GPIO.cleanup()
