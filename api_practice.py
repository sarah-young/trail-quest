import requests
import secrets
from requests import sessions


api_key = secrets.HIKING_PROJECT_API_KEY

lat = "37.788801" 
lon = "-122.411478"


data_request = requests.get("https://www.hikingproject.com/data/get-trails?lat="+lat+"&lon="+lon+"&minLength=1&maxResults=500&key="+api_key)

request_json = data_request.json()

trail_data = request_json["trails"]

counter = 0
for trail in trail_data:
	counter += 1
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
	print "<TRAIL "+str(counter)+">"
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



# BRAINSTORMING API PRACTICE #
###################################################


# r_usfs = requests.get("https://ridb.recreation.gov/api/v1/trails/USFS?offset=100&milesmin=1&limit=50&apikey="+api_key)
# usfs_trails_json = r_usfs.json()
# # trails from the United States Forest Service


# r_fws = requests.get("https://ridb.recreation.gov/api/v1/trails/FWS?apikey="+api_key)
# fws_trails_json = r_fws.json()x	
# # trains from FWS


# # print trails_json

# usfs_trail = usfs_trails_json["RECDATA"]



# for i in usfs_trail: 
# 	trail_name = i['TrailName']
# 	trail_length = i['GISMiles']
# 	lat_long = i.get('GEOM') # <-- GPS trail coordinates; in long/lat fomat
# 	print lat_long
	
# 	address = i.get('Address')
# 	use = i.get('ManageUse')
# 	if address is not None:
# 		address_split = address.split(',')
# 		print address_split

# 	print trail_name, " | ", trail_length
		
# # first_trail = trail["TrailName"]
# # print first_trail



# fws_trail = fws_trails_json["RECDATA"]

# for i in fws_trail:
# 	if int(i.get('SecLength')) > 1:
# 		# only show trails that are > 1 mile in length
# 		print i['Name'], i.get('SecLength', 'NO SECTION LENGTH'), i.get('TrailNo'), i.get('TrailFrom'), i.get('TrailTo'), i.get('Address')