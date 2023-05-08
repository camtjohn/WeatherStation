import os, time, threading
import weather_module as weather
import led_module

list_led = led_module.list_led

##################
def sleep_thread():
    #turn off display
    led_module.off_all()
    global config
    config = 'sleeping'

def start_sleep_timer():
	sec_till_sleep = 5
	threading.Timer(sec_till_sleep, sleep_thread).start()
##################    
    

def button_pressed(btn):
    start_sleep_timer()
    filter_calls(btn)


config = ' '

def filter_calls(btn):
    global config
    
    if config == 'sleeping':
        if btn == 5:
            #led fun (or temp that day?)
            print('i was sleeping')
            led_module.blink(list_led[4])
        elif btn == 6:
            #led fun
            led_module.blink(list_led[5])
        elif btn == 7:
            #led fun
            led_module.blink(list_led[6])
        elif btn == 8:
            #led fun
            led_module.blink(list_led[7])
        elif btn == 9:
            #led fun
            led_module.blink(list_led[8])
            
    elif config == 'temp':
        if btn == 1:
            print(weather.current_temp)
        if btn == 5:
            #display date0 min/max, led5=on
            led_module.blink(list_led[4])
            print(weather.day0['min'], weather.day0['max'], weather.reception_time)
        elif btn == 6:
            #display date0 min/max, led5=on
            led_module.blink(list_led[5])
            print(weather.day1['min'], weather.day1['max'])
        elif btn == 7:
            #display date0 min/max, led5=on
            led_module.blink(list_led[6])
            print(weather.day2['min'], weather.day2['max'])
        elif btn == 8:
            #display date0 min/max, led5=on
            led_module.blink(list_led[7])
            print(weather.day3['min'], weather.day3['max'])
        elif btn == 9:
            #display date0 min/max, led5=on
            led_module.blink(list_led[8])
            print(weather.day4['min'], weather.day4['max'])
            
    if btn == 1:
        #activate temp
        config = 'temp'
        led_module.off_all()
        led_module.on(list_led[0])
    elif btn == 2:
        #activate rain, led=on for days w/ rain
        config = 'rain'
        led_module.off_all()
        led_module.on(list_led[1])
        print('Rain activated')
    elif btn == 3:
        #activate_sunset, display sunset_time
        config = 'sunset'
        led_module.off_all()
        led_module.on(list_led[2])
        print('Sunset at: ',weather.sunset_time)
    elif btn == 4:
        #activate moon, display moon_days
        config = 'moon'
        led_module.off_all()
        led_module.on(list_led[3])
        print('Moon phase here')
                

