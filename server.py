from flask import Flask, render_template, request, session, jsonify
import secrets
import functions
from flask import Flask, redirect, request, render_template, session, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db
import model

app = Flask(__name__)

app.secret_key = "SECRETSECRETSECRET"


@app.route('/')
def display_trail_form():
	"""Displays form that takes in user input"""

	if session.get('username'):
	# check to see if username is in the session --if not, login page!
		return render_template('/homepage.html')
	else:
		flash("Please login to begin your adventure.")
		return render_template('/welcome.html')
		# This should be complete?

@app.route('/trails_asychronous', methods=['POST'])
def asynchronous_info_load():

	# import pdb; pdb.set_trace()

	print "REQUEST FORM DATA: ", request.form.get("data")
	city = request.form.get("city")
	print "CITY: ", city
	state = request.form.get("state")
	print "STATE: ", state
	radius = request.form.get("radius")
	print "RADIUS: ", radius
	trek_length = request.form.get("trek_length")
	print "TREK LENGTH: ", trek_length
	trail_difficulty = request.form.get("trail_difficulty")
	print "DIFFICULTY SELECTED: ", trail_difficulty

	coordinates = functions.find_lat_lng(city,state)
	# ***Google Map API gets called here!***
	print "COORDINATES: ", coordinates

	radius_to_meters = int(radius) * 1609.34

	if coordinates == None:
		print "!!!LOCATION OR RANGE ERROR!!!"
		return "FOO"

	trails = functions.find_trails(coordinates, radius)
	# ***Hiking API gets called here!***

	if len(trails) == 0:

		print "!!!LOCATION OR RANGE ERROR!!! NO TRAILS"
		return "BAR"

	trails_to_db = functions.add_trails_to_db(trails)
	# Adds all trails from hiking project API to database
	trails = functions.filter_trek_length(trails, trek_length)
	# filters trail returned by API by user trail length preference
	print "TRAILS AFTER LENGTH FILTER: ", trails

	trails = functions.filter_trek_difficulty(trails, trail_difficulty)
	# filters trails returned by API for user trail difficulty preference

	print "TRAILS AFTER DIFFICULTY FILTER: ", trails

 	selected_trails = functions.select_three_trails(trails)
		# If selected trails == none, send back STRING which triggers different
		# in JavaScript
	print "SELECTED TRAILS OBJECT TYPE: ", type(selected_trails)
	print
	lat, lng = coordinates
	lat = float(lat)
	lng = float(lng)

	selected_trails[0]["city_lat"] = float(lat)
	selected_trails[0]["city_long"] = float(lng)
	selected_trails[0]["radius_in_meters"] = radius_to_meters
	print "SELECTED TRAILS: ", selected_trails
	session['radius'] = radius_to_meters

	if selected_trails > 1:
		return jsonify(selected_trails)
	# Keeping for now to see if this works with other routes... Not sure if this is needed.

	else:
		print "***LOCATION OR RANGE ERROR***"
		return "STRING"


@app.route('/trails')
def display_selected_trails():
	"""Display trails selected by select_three_trails"""

	selected_trails = session['selected_trails']
	print "SELECTED TRAILS: ", selected_trails
	city, state = session['location']
	print "CITY/STATE: ", city, state

	google_maps_api_key = secrets.SATELLITE_MAP_GM_API_KEY

	coordinates = session['coordinates'] # lat / long from Google Maps API call
	lat, lng = coordinates
	city_latitude = float(lat)
	city_longitude = float(lng)
	radius_in_meters = session['radius']
	# this isn't needed anymore? Or is it??? Maybe this is easier than sending stuff back and forth??? Keep this for now..

	return render_template('/trails.html', selected_trails=selected_trails, city=city, state=state, api_key=google_maps_api_key, city_latitude=lat, city_longitude=lng, radius=radius_in_meters)
	# passing selected_trails list, city, state, api key for google maps, and lat/long for map


@app.route('/welcome')
def show_registration_page():
	"""Show user registration form"""

	return render_template('/welcome.html')

@app.route('/register', methods=['POST'])
def register_user():
	"""Take entries from registration form, check to see if user is in database.

	If user is not in database, add to database and redirect to login page w/
	appropriate flash message.
	If user is in database, redirect to login page w/ appropriate flash message"""

	username = request.form.get("username")
	password = request.form.get("password")

	a_new_user = functions.add_user_to_database(username, password)

	if a_new_user:

		flash("Thanks for registering for Trail Quest! Please login.")
		return render_template('/login.html')
	else:
		flash("User already in database. Please login with credentials.")
		return render_template('/login.html')

@app.route('/login', methods=['POST'])
def user_login():
	"""Take user login information, check database, return:
		> Homepage if user login information is correct w/ appropriate flash
		message
		> Welcome page if user login information is incorrect w/ appropriate
		flash message.
	"""
	username = request.form.get("loginemail")
	password = request.form.get("loginpassword")
	password_check = check_user_credentials(username, password)
	# TODO: Make function to check deets

	if password_check:
		flash('Logged in successfully.')
		session['user_id'] = user.user_id
		return render_template('/homepage.html')

	else:
		flash('Please try your login again.')
		return render_template('/welcome.html')

@app.route('/logout', methods=["POST"])
def user_logout():
	"""When logout button is selected:
	> delete current session key
	> add flash message
	> return render_template ('welcome.html')"""
	pass

@app.route('/trek')
def show_trail_location():
	"""Displays trail location on map and more information about the trail."""

	# TODO: Refactor so this works with the one-page app format
	# FIXME: Question: How do I pass the user_id here? JSON???


	chosen_trail_id = request.args.form.get()
	trail_conditions = functions.get_trail_conditions(chosen_trail_id)
	# calls Hiking Project API to get trail conditions for specific hike
	chosen_trail = model.Trail.query.filter_by(trail_id=chosen_trail_id).first()
	# trail_map = functions.get_map(str(chosen_trail.trailhead_latitude), str(chosen_trail.trailhead_longitude))
	# print trail_map
	# get trailhead coordinates from trail object for map
	print "***TYPE***", type(chosen_trail)

	return render_template('/trek.html', trek=chosen_trail, trail_conditions=trail_conditions)


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')
