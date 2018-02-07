"""Search Functionality Rough Draft"""
import secrets
import requests

gm_api_key = secrets.GOOGLE_MAPS_API_KEY
hp_api_key = secrets.HIKING_PROJECT_API_KEY

city = raw_input('City: ')
state = raw_input('State: ')
radius = raw_input('Distance: ')

geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+state+"&key="+gm_api_key)
json_geocode = geocode_request.json()
lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
lat = str(lat)
lng = str(lng)

trail_request = requests.get("https://www.hikingproject.com/data/get-trails?lat="+lat+"&lon="+lng+"&maxDistance="+radius+"&minLength=1&key="+hp_api_key)

trail_packet = trail_request.json()

trail_data = trail_packet["trails"]

for trail in trail_data:
	trail_id = trail['id']
	trail_name = trail['name']
	trailhead_longitude = trail['longitude']
	trailhead_latitude = trail['latitude']
	trail_length = trail['length']
	trail_difficulty = trail['difficulty']
	trail_description = trail['summary']
	trail_high_alt = trail['high']
	trail_low_alt = trail['low']
	trail_location = trail['location']
	picture = trail['imgMedium']

	print "Trail ID:",trail_id
	print "Trail Name:",trail_name
	print "Longitude:",trailhead_longitude
	print "Latitude:",trailhead_latitude
	print "Length:",trail_length
	print "Difficulty:",trail_difficulty
	print "Description:",trail_description
	print "High point:",trail_high_alt
	print "Low point:",trail_low_alt
	print "Location:",trail_location
	print "Image link:", picture
	print 