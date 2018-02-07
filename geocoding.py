import secrets
import requests

api_key = secrets.GOOGLE_MAPS_API_KEY

city = 'Mountain View'
state = 'CA'

geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+city+state+"&key="+api_key)
json_geocode = geocode_request.json()
#print json_geocode

lat,lng = json_geocode['results'][0].get('geometry').get('location').values()
print lat_lng

lat, lng = lat_lng
print lat
print lng




