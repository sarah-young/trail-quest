from flask import Flask, render_template, request, session
import secrets
import functions
from flask import Flask, redirect, request, render_template, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db

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
	session['selected_trails'] = functions.select_three_trails(trails)

	return redirect('/trails')

@app.route('/trails')
def display_selected_trails():
	"""Display trails selected by select_three_trails"""
	 #selected_trails=selected_trails

	selected_trails = session['selected_trails']

	return render_template('/trails.html', selected_trails=selected_trails)


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')




