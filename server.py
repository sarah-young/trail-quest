from flask import Flask, render_template, request, session
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

	return render_template('/homepage.html')


@app.route('/trail_selector')
def search_with_user_data():
	"""Take im data and pass to relevant functions"""

	city = request.args.get("city")
	state = request.args.get("state")
	radius = request.args.get("radius")
	trek_length = request.args.get("trek_length")
	difficulty = request.args.get("difficulty")


	coordinates = functions.find_lat_lng(city,state)
	if coordinates == None:
		flash("Hmm. No trails were found. Try another location?")
		return render_template('/homepage.html')
	trails = functions.find_trails(coordinates, radius)
	if len(trails) == 0:
		flash("Hmm. No trails were found. Try another location?")
		return render_template('/homepage.html')

	trails_to_db = functions.add_trails_to_db(trails)
	session['selected_trails'] = functions.select_three_trails(trails)
	session['location'] = (city, state,)
	

	return redirect('/trails')

@app.route('/trails')
def display_selected_trails():
	"""Display trails selected by select_three_trails"""

	selected_trails = session['selected_trails']
	city, state = session['location']

	return render_template('/trails.html', selected_trails=selected_trails, city=city, state=state)


@app.route('/trek')
def show_trail_location():
	"""Displays trail location on map and more information about the trail."""

	chosen_trail_id = request.args.get("trail_id")
	trail_conditions = functions.get_trail_conditions(chosen_trail_id)
	# calls Hiking Project API to get trail conditions for specific hike
	chosen_trail = model.Trail.query.filter_by(trail_id=chosen_trail_id).first()
	# trail_map = functions.get_map(str(chosen_trail.trailhead_latitude), str(chosen_trail.trailhead_longitude))
	# print trail_map
	# figuring out which Google Maps API I should use
	# get trailhead coordinates from trail object for map
	print "***TYPE***", type(chosen_trail)

	return render_template('/trek.html', trek=chosen_trail, trail_conditions=trail_conditions) #, trail_map = trail_map)


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')





