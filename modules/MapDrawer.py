import numpy as np
import requests
import json
import polyline
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn import preprocessing 
from tools.WeatherFunctions import *

ORIGIN = "Hoyanger,NOR"
DESTINATION = "Brendeholten,Forde,NOR"
# ORIGIN = "Tromso,NOR"
# DESTINATION = "Oksfjord,NOR"
GOOGLE_ROUTING_URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}"


def getCoordinates(Origin, Destination):
    try:
        url = GOOGLE_ROUTING_URL.format(Origin, Destination)
        r = requests.get(url)
        travelRoute_json = json.loads(r.text)
        polyline_json = travelRoute_json['routes'][0]['overview_polyline']['points']
        polyline_coord = polyline.decode(polyline_json)
        coordinates = np.array(polyline_coord)
        return coordinates
    except:
        print("Could not connect to google.")
        return None

def normaliseArray(Array):
    array_norm = preprocessing.MinMaxScaler().fit_transform(Array)
    return array_norm

def convSpherCoordTo2D(Array):
    # Opplosning for konvertering fra sfaeriske koordinater
    # til 2D for plotting av riktig aspektratio.
    MAP_WIDTH = 1024
    MAP_HEIGHT = 1024

    lon = [((MAP_WIDTH/360) * (180 + lon)) for lon in Array[:,1]]
    lat = [((MAP_HEIGHT/180) * (90 + lat)) for lat in Array[:,0]]
    return lon, lat

def plotLatLonColor(myCoord, ChunkNo):
    MAXTEMP = 30
    MINTEMP = 24
    lon, lat = convSpherCoordTo2D(myCoord)
    NoEntries = len(lon)
    CoorDistance = NoEntries / ChunkNo
    LastChunk = 0
    ColorArray =[]

    for ent in range(NoEntries):
        if ent % CoorDistance == 0:
            # print(myCoordinates[ent,1])
            # print(myCoordinates[ent,0])
            localweather = minWeatherAtLocation(myCoord[ent,1], myCoord[ent,0])
            if localweather >= MAXTEMP:
                RGBvalue = 1
            elif localweather <= MINTEMP:
                RGBvalue = 0
            else:
                RGBvalue = (MAXTEMP - localweather) / (MAXTEMP - MINTEMP)
            # print(myCoordinates[ent], RGBvalue)

        ColorArray.append(RGBvalue)

    
    return lon, lat, ColorArray



myCoordinates = getCoordinates(ORIGIN,DESTINATION)
lon, lat, colors = plotLatLonColor(myCoordinates, 5)

plt.gca().set_aspect('equal', adjustable='box')
plt.scatter(lon,lat, c=colors)
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




# '''
# MAPQUEST VERSION


# '''

# MAPQUEST_API_KEY = "iHxguh7lz7PkRssOrO4XHoVL5vQWNRb8"
# '''
# routeTypes: fastest, shortest, pedestrian, multimodal, bicycle
# unit: m / km
# '''
# routetype = "shortest"

# MAPQUEST_API = "https://www.mapquestapi.com/directions/v2/route?key={0}&from={1}&to={2}&outFormat=json&ambiguities=ignore&routeType={3}&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false&unit=k"
# def getDirection_MAPQUEST(origin, destination, routetype):
#     url = MAPQUEST_API.format(MAPQUEST_API_KEY, origin, destination,routetype)
#     # print url
#     r = requests.get(url)
#     response_json = json.loads(r.text)
#     return response_json['route']
# response = getDirection_MAPQUEST(Origin, Destination, "fastest")
# total_distance = 0

# for leg in response['legs']:
#     for maneuver in leg['maneuvers']:
#         # pprint(maneuver['startPoint'])
#         total_distance += maneuver['distance']
# print("total time: {}".format(str(response['formattedTime'])))
# print("total distance: {}".format(str(total_distance)+ " km"))


# #for point in responses:

