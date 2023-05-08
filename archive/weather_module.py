import time
import pyowm
import datetime
import threading
import led_module


# convert unix gmt to string cdt
def gmt_to_cdt(unix_gmt):
	string_cdt = datetime.datetime.fromtimestamp(int(unix_gmt)).strftime('%Y-%m-%d %H:%M:%S')
	
	return string_cdt


# Establish dictionaries for each day = {date, min, max, rain, moon, sunset_time}
day0 = {}
day1 = {}
day2 = {}
day3 = {}
day4 = {}

days = [day0, day1, day2, day3, day4] #list of dictionary days



def weather_api():	
	# Append dates to list of days
	one_day = datetime.timedelta(days = 1)
	
	date0 = datetime.datetime.today()
	date1 = date0 + one_day
	date2 = date1 + one_day
	date3 = date2 + one_day
	date4 = date3 + one_day
	
	time0 = date0.strftime('%H:%M:%S')
	
	day0['date'] = date0.strftime('%Y-%m-%d')
	day1['date'] = date1.strftime('%Y-%m-%d')
	day2['date'] = date2.strftime('%Y-%m-%d')
	day3['date'] = date3.strftime('%Y-%m-%d')
	day4['date'] = date4.strftime('%Y-%m-%d')

	
	# Pull weather data from OpenWeatherMap API
	owm = pyowm.OWM('3836f65abd758ae760af5f75471fe0b1')

	observation = owm.weather_at_place('78702')
	w = observation.get_weather()
	reception_time = observation.get_reception_time(timeformat='iso')
	temp = w.get_temperature('fahrenheit')
	current_temp = temp['temp']
	rainfall = w.get_rain()

	sunset_gmt = w.get_sunset_time()
	sunset = gmt_to_cdt(sunset_gmt)
	#d = datetime.strptime(sunset, '%H:%M:%S')
	#d2 = datetime.strftime(%I:%M %p)
	sunset_time = sunset.split()[1]
	
	
	austin = owm.three_hours_forecast('78702')
	forecast = austin.get_forecast()
	
	# Grab rain forecast and temperatures for each day
	forecast_dict = {}
	temp_min_dict = {}
	temp_max_dict = {}
	
	# for each record in forecast (once every 3 hours for 5 days)
	for weather in forecast:
		dt_gmt = weather.get_reference_time() #grab date+time of record
		dt = gmt_to_cdt(dt_gmt)
		date = dt.split()[0]
		time = dt.split()[1]
		
		status = weather.get_status() #grab weather(cloudy, rain, clear)
		
		temps = weather.get_temperature('fahrenheit') #grab temp min, max
		temp_min = temps['temp_min']
		temp_max = temps['temp_max']
		
		# assign weather, temp min, temp max to corresponding local dictionaries
		if date in forecast_dict:
			forecast_dict[date].append(status)
			temp_min_dict[date].append(temp_min)
			temp_max_dict[date].append(temp_max)
		else:
			forecast_dict[date] = []
			temp_min_dict[date] = []
			temp_max_dict[date] = []
			forecast_dict[date].append(status)
			temp_min_dict[date].append(temp_min)
			temp_max_dict[date].append(temp_max)


	time_now = datetime.datetime.now()
	time_late = datetime.datetime.strptime('21','%H')

	# allot temp min/max and rain into day dictionaries
	for day in days:
		#if the time now is after 9pm(21:00), there's no data to show for today
		if time_now.time() > time_late.time() and day['date']==day0['date']: 
			day['rain'] = rainfall
			day['min'] = 'todays min'
			day['max'] = 'todays max'
		else:
			date = day['date']
			day['min'] = min( temp_min_dict[date] )
			day['max'] = max( temp_max_dict[date] )
			day['rain'] = 'Rain' in forecast_dict[date]
	
	return rainfall, sunset_time, current_temp, reception_time	#rain and temps recorded to dictionaries

rainfall, sunset_time, current_temp, reception_time = weather_api()


def send_days():
	return days



# Find the number of seconds until next call to the API
def time_till_call():
	now = datetime.datetime.today()
	date_today = now.strftime('%Y-%m-%d')
	
	one_day = datetime.timedelta(days = 1)
	datetime_tomorrow = now + one_day
	date_tomorrow = datetime_tomorrow.strftime('%Y-%m-%d')
	
	
	call_time = []
	call_time.append(date_today + ' 01:01:00')
	call_time.append(date_today + ' 04:01:00')
	call_time.append(date_today + ' 07:01:00')
	call_time.append(date_today + ' 16:01:00')
	call_time.append(date_today + ' 19:01:00')
	
	
	####TESTING STUFF#####
	call_interval = datetime.timedelta(seconds = 30)
	
	test = []
	for x in range(10):
		test_datetime = now + call_interval
		test.append(test_datetime.strftime('%H:%M:%S'))

	for x in range(len(test)):
		call_time.append(date_today + ' ' + test[x])
	######################
	
	
	# find the time interval between now and call times 
	time_delta = []
	i = 0
	while i < len(call_time):
		call = datetime.datetime.strptime(call_time[i],'%Y-%m-%d %H:%M:%S')
		time_difference = (call - now).total_seconds()
		if time_difference > 0:
			time_delta.append(time_difference)
		i += 1
	
	
	# find minimum positive interval. if none than go to tomorrows 1st interval
	
	if len(time_delta) > 0:
		sec_till_run = min(time_delta)
	else:
		call_datetime = date_tomorrow + ' 01:01:00'
		call = datetime.datetime.strptime(call_datetime,'%Y-%m-%d %H:%M:%S')
		time_difference = (call - now)
		sec_till_run = time_difference.total_seconds()
		
	return sec_till_run

sec_till_run = time_till_call()

# start this thread in order to call weather API. then start new timer.
def thread_fn():
	global rainfall
	global sunset_time
	global reception_time
	global sec_till_run
	
	rainfall, sunset_time, current_temp, reception_time = weather_api()

	
	sec_till_run = time_till_call()
	print('Seconds until next call: ', sec_till_run)
	
	start_timer()

# intiate countdown to call the thread function
def start_timer():
	threading.Timer(sec_till_run, thread_fn).start()

