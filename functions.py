"""Functions for Trail Quest"""

import secrets
import requests
import random
import model
#from flask_sqlalchemy import SQLAlchemy
from flask import Flask

gm_api_key = secrets.GOOGLE_MAPS_API_KEY
hp_api_key = secrets.HIKING_PROJECT_API_KEY
satellite_map_api_key =secrets.SATELLITE_MAP_GM_API_KEY

#db = SQLAlchemy()

def find_lat_lng(city, state):
	"""
	Find lat/long for address given by user. 

	Uses Google Maps API & Hiking Project API.
	
	Information passed from HTML form to this function. 

	"""
	try:
		geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+state+"US&key="+gm_api_key)
		json_geocode = geocode_request.json()
		lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
		coordinates = (str(lat),str(lng),)

		return coordinates

	except:
		return None



def find_trails(coordinates, radius):
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


def select_three_trails(trails, trek_length, trail_difficulty):
	"""Selects three random trails from trail_packet from find_trails"""

	trail_list = []

	for trail in trails: 
		if trail.trail_length <= trek_length:
			if trail.trail_difficulty == difficulty:
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


def add_trails_to_db(trails):
	"""Adds user selected trail to db"""

	for trail in trails:
		print len(trails)
		print trail['name']
		print type(trail)
		trail_object = model.Trail(trail_id = trail['id'],
					  trail_name = trail['name'],
					  trailhead_latitude = trail['latitude'],
					  trailhead_longitude = trail['longitude'],
					  trail_length = trail['length'],
					  trail_difficulty = trail['difficulty'],
					  trail_description = trail['summary'],
					  trail_high_alt = trail['high'],
					  trail_low_alt = trail['low'],
					  trail_location = trail['location'],
					  trail_picture = trail['imgMedium'])

		trail_status = model.db.session.query(model.Trail).filter(model.Trail.trail_id==trail['id']).first()
		if trail_status == None:
			model.db.session.add(trail_object)
			model.db.session.commit()
			print "<Added trail %s to database>" % trail['id']
		else:
			print "<Trail %s is already in the database>"



def get_trail_conditions(trail_id):
	"""Calls Hiking Project API for trail conditions using trail_id."""

	trail_id = str(trail_id)
	conditions_request = requests.get("https://www.hikingproject.com/data/get-conditions?ids="+trail_id+"&key="+hp_api_key)
	json_conditions = conditions_request.json()
	fetch = json_conditions["0"]
	trail_name_by_id = fetch.get("name")#.values()
	print trail_name_by_id
	trail_status_details =fetch.get("conditionStatus")#.values()
	print trail_status_details
	trail_status_color = fetch.get("conditionColor")#.values()
	print trail_status_color
	trail_status_date = fetch.get("conditionDate")

	if trail_status_date.startswith("1970"):
	# Checks to see if there's a relevant trail condition report
		trail_deets = None
		print "NO REPORT AVAILABLE"
		return trail_deets
	elif trail_status_details.lower().startswith("unknown"):
		trail_deets = None
		print "NO REPORT AVAILABLE"
		return trail_deets

	trail_deets = (trail_name_by_id, trail_status_details, trail_status_color, trail_status_date,)

	return trail_deets


def get_map(lat, lng):
	"""Gets map information based on coordinates"""

	# map_based_on_coordinates = "https://www.google.com/maps/embed/v1/view?key="+satellite_map_api_key+"&center="+lat+","+lng+"&zoom=18&maptype=satellite"
	# view only map; no markers seemingly available &  no dirxns

	pass

	#return map_based_on_coordinates

	# "0": {
 #        "id": 7000108,
 #        "name": "Angels Landing",
 #        "url": "https:\/\/www.hikingproject.com\/trail\/7000108\/angels-landing",
 #        "urlConditionsHistory": "https:\/\/www.hikingproject.com\/trail\/7000108\/angels-landing?modal=trail-conditions-modal",
 #        "urlConditionsUpdate": "https:\/\/www.hikingproject.com\/trail\/7000108\/angels-landing?action=update-conditions",
 #        "conditionStatus": "All Clear",
 #        "conditionColor": "Green",
 #        "conditionDetails": "",
 #        "conditionImg": "https:\/\/cdn.apstatic.com\/img\/conditions\/green.svg",
 #        "conditionDate": "2018-02-01 14:28:02"





########TESTS & STUFF##########

# test_list = []
# test1 = select_three_trails(test_list)
# print test1


