from flask import Flask, render_template
import secrets
import requests
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db

app = Flask(__name__)

app.secret_key = "SECRETSECRETSECRET"

@app.route('/homepage')
def search_for_trails():
	"""Take in user input and search for trails based on location & distance from location"""

	gm_api_key = secrets.GOOGLE_MAPS_API_KEY
	hp_api_key = secrets.HIKING_PROJECT_API_KEY


	city = request.args.get("city")
	state = requests.args.get('state')
	distance = requests.args.get('distance')

	geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+state+"&key="+gm_api_key)
	json_geocode = geocode_request.json()
	lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
	lat = str(lat)
	lng = str(lng)

	trail_request = requests.get("https://www.hikingproject.com/data/get-trails?lat="+lat+"&lon="+lng+"&maxDistance="+distance+"&minLength=1&key="+hp_api_key)

	trail_packet = trail_request.json()

	trail_data = trail_packet["trails"]

	return render_template('trailselector.html', trail_data=trail_data)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()


