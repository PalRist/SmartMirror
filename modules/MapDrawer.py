import numpy as np
import requests
import json
import polyline
from pprint import pprint
from sklearn import preprocessing 

Origin = "Hoyanger,NOR"
Destination = "Brendeholten,Forde,NOR"
GOOGLE_ROUTING_URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}"


def getCoordinates(Origin, Destination):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}".format(Origin, Destination)
    r = requests.get(url)
    travelRoute_json = json.loads(r.text)
    polyline_json = travelRoute_json['routes'][0]['overview_polyline']['points']
    polyline_coord = polyline.decode(polyline_json)
    coordinates = np.array(polyline_coord)

    # lan_max, lan_max = coordinates.max(axis=0)
    # lon_max, lon_min = coordinates.min(axis=0)
    return coordinates

def normaliseArray(Array):
    array_norm = preprocessing.MinMaxScaler().fit_transform(Array)
    return array_norm

def getDirections(origin, destination):
    '''
    :param origin: Start destination
    :param destination: End destination
    :return array of destinations -
    '''
    url = GOOGLE_ROUTING_URL.format(Origin, Destination)
    try:
        r = requests.get(url)
        response_json = json.loads(r.text)
        return response_json['routes']

    except requests.ConnectionError:
        '''
        Do something smart when this happens
        '''
        print("Connection error")
        return None






a = getCoordinates(Origin, Destination)
print(normaliseArray(a))


json_response = getDirections(Origin, Destination)

for direction in json_response:
    points = direction['overview_polyline']['points']
    polyline_coord = polyline.decode(points)
    # print polyline_coord


'''
MAPQUEST VERSION


'''

MAPQUEST_API_KEY = "iHxguh7lz7PkRssOrO4XHoVL5vQWNRb8"
'''
routeTypes: fastest, shortest, pedestrian, multimodal, bicycle
unit: m / km
'''
routetype = "shortest"

MAPQUEST_API = "https://www.mapquestapi.com/directions/v2/route?key={0}&from={1}&to={2}&outFormat=json&ambiguities=ignore&routeType={3}&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false&unit=k"
def getDirection_MAPQUEST(origin, destination, routetype):
    url = MAPQUEST_API.format(MAPQUEST_API_KEY, origin, destination,routetype)
    # print url
    r = requests.get(url)
    response_json = json.loads(r.text)
    return response_json['route']
response = getDirection_MAPQUEST(Origin, Destination, "fastest")
total_distance = 0

for leg in response['legs']:
    for maneuver in leg['maneuvers']:
        # pprint(maneuver['startPoint'])
        total_distance += maneuver['distance']
print("total time: {}".format(str(response['formattedTime'])))
print("total distance: {}".format(str(total_distance)+ " km"))


#for point in responses:

