from flask import Flask, render_template, request
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


@app.route('trail_selector')
def search_with_user_data():
	"""Take im data and pass to relevant functions"""

	address = request.args.get("address")
	city = request.args.get("city")
	state = request.args.get("state")
	travel_distance = request.args.get('travel_distance')
	# trek_length = 

	return redirect ('/trails', select_trails = select_trails)

@app.route('/trails')
def display_selected_trails(select_trails):
	"""Display trails selected by select_three_trails"""


	return render_template('/trails.html')


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')




