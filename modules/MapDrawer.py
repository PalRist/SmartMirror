import numpy as np
import requests
import json
import polyline
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn import preprocessing 

ORIGIN = "Hoyanger,NOR"
DESTINATION = "Brendeholten,Forde,NOR"
# ORIGIN = "Tromso,NOR"
# DESTINATION = "Oksfjord,NOR"
GOOGLE_ROUTING_URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}"


def getCoordinates(Origin, Destination):
    url = GOOGLE_ROUTING_URL.format(Origin, Destination)
    r = requests.get(url, verify=False)
    travelRoute_json = json.loads(r.text)
    polyline_json = travelRoute_json['routes'][0]['overview_polyline']['points']
    polyline_coord = polyline.decode(polyline_json)
    coordinates = np.array(polyline_coord)
    return coordinates

def normaliseArray(Array):
    array_norm = preprocessing.MinMaxScaler().fit_transform(Array)
    return array_norm

def convSpherCoordTo2D(Array):
    '''
    Oppløsning for konvertering fra sfæriske koordinater
    til 2D for plotting av riktig aspektratio.
    '''
    MAP_WIDTH = 1024
    MAP_HEIGHT = 1024
    
    newX = [((MAP_WIDTH/360) * (180 + lon)) for lon in Array[:,1]]
    newY = [((MAP_HEIGHT/180) * (90 + lan)) for lan in Array[:,0]]
    return newX, newY

TheMap = getCoordinates(ORIGIN,DESTINATION)
lon, lan = convSpherCoordTo2D(TheMap)

plt.gca().set_aspect('equal', adjustable='box')
plt.plot(lon,lan)
plt.show()

# Trengs denne funksjonen?
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

