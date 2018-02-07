"""Functions for Trail Quest"""

import secrets
import requests
import random

gm_api_key = secrets.GOOGLE_MAPS_API_KEY
hp_api_key = secrets.HIKING_PROJECT_API_KEY


def find_lat_lng(city, state, address=None):
	"""
	Find lat/long for address given by user. 

	Uses Google Maps API & Hiking Project API.
	
	Information passed from HTML form to this function. 

	"""

	geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+state+"&key="+gm_api_key)
	json_geocode = geocode_request.json()
	lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
	coordinates = (str(lat),str(lng),)

	return coordinates


def find_trails(coordinates):
	"""Find trails based on GPS coordinates from find_lat_lng
	
	Uses Hiking Project API

	"""

	lat, lng = coordinates
	# Unpacking coordinates from Google Maps API
	trail_request = requests.get("https://www.hikingproject.com/data/get-trails?lat="+lat+"&lon="+lng+"&maxDistance="+radius+"&minLength=1&key="+hp_api_key)
	# Requesting trails near GPS coordinate from Hiking Project API
	trail_packet = trail_request.json()
	# 
	trails = trail_packet["trails"]

	return trails


def select_three_trails(trails):
	"""Selects three random trails from trail_packet from find_trails"""

	trail_list = []

	for trail in trails: 
		trail_list.append(trail)

	if len(trail_list) == 0:
		return None	
		# return something that prompts server.py route to add a flash message

	elif len(trail_list) < 4:
		selected_trails = trail_list
		# give message on route side that states user may want to widen search criteria

		return selected_trails

	elif len(trail_list) >=4:
		selected_trails = []
		random.shuffle(trail_list)
		first_trail = trail_list.pop()
		selected_trails.append(first_trail)
		second_trail = trail_list.pop()
		selected_trails.append(second_trail)
		third_trail = trail_list.pop()
		selected_trails.append(third_trail)

		return selected_trails


########TESTS & STUFF##########

# test_list = []
# test1 = select_three_trails(test_list)
# print test1


