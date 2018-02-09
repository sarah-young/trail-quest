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
	radius = '25'
	# trek_length = 

	coordinates = functions.find_lat_lng(city,state)
	trails = functions.find_trails(coordinates, radius)
	if len(trails) == 0:
		flash("Hmm. No trails were found. Try another location?")
		return render_template('/homepage.html')

	trails_to_db = functions.add_trails_to_db(trails)
	session['selected_trails'] = functions.select_three_trails(trails)
	

	return redirect('/trails')

@app.route('/trails')
def display_selected_trails():
	"""Display trails selected by select_three_trails"""

	selected_trails = session['selected_trails']

	return render_template('/trails.html', selected_trails=selected_trails)


@app.route('/trek')
def show_trail_location():
	"""Displays trail location on map and more information about the trail."""

	chosen_trail_id = request.args.get("trail_id")
	print "*******TRAIL ID: ",chosen_trail_id,"**********"
	chosen_trail_object = model.Trail.query.filter_by(trail_id=chosen_trail_id).first()
	print type(chosen_trail_object)
	session['chosen_trail_object'] = chosen_trail_object
	trek = session['chosen_trail_object']
	# saving to session to allow for use on other pages & saving in database

	return render_template('/trek.html', trek=trek)


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')





