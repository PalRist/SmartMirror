#!/usr/bin/env python3


import numpy as np
import requests
import json
import polyline


Origin = "Hoyanger,NO"
Destination = "Brendeholten,Forde,NO"

def GetMapCoordinates(Origin, Destination):

	url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s" % (Origin, Destination)
	r = requests.get(url, verify=False)
	travelRoute_json = json.loads(r.text)
	polyline_json = travelRoute_json['routes'][0]['overview_polyline']['points']
	polyline_coord = polyline.decode(polyline_json)
	coordinates = np.array(polyline_coord)

	# print(coordinates[0][0])
	# lan_max, lan_max = coordinates.max(axis=0)
	# lan_min, lan_min = coordinates.min(axis=0)

	coordinates_norm = np.apply_along_axis(np.linalg.norm, 1, coordinates)
	print(coordinates_norm)


GetMapCoordinates(Origin, Destination)


	