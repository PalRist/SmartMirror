import numpy as np
import requests
import json
import polyline
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn import preprocessing 
from tools.WeatherFunctions import *

myORIGIN = "Hoyanger,NOR"
myDESTINATION = "Brendeholten,Forde,NOR"
# ORIGIN = "Tromso,NOR"
# DESTINATION = "Oksfjord,NOR"
GOOGLE_ROUTING_URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}"


def getCoordinates(Origin, Destination):
    '''
    Queries google for map coordinates between two locations.
    '''
    try:
        url = GOOGLE_ROUTING_URL.format(Origin, Destination)
        r = requests.get(url, timeout=10)
        travelRoute_json = json.loads(r.text)
        pprint(travelRoute_json['routes'])
        polyline_json = str(travelRoute_json['routes']['0']['overview_polyline']['points'])

        polyline_coord = polyline.decode(polyline_json)
        coordinates = np.array(polyline_coord)
        return coordinates
    except:
        print("Could not connect to google.")
        quit()

def normaliseArray(Array):
    array_norm = preprocessing.MinMaxScaler().fit_transform(Array)
    return array_norm

def convSpherCoordTo2D(Array):
    '''
    Converts map/spherical coordinates to 2D coordinates
    '''
    MAP_WIDTH = 1024
    MAP_HEIGHT = 1024

    lon = [((MAP_WIDTH/360) * (180 + lon)) for lon in Array[:,1]]
    lat = [((MAP_HEIGHT/180) * (90 + lat)) for lat in Array[:,0]]
    return lon, lat

def colorCodeTemperature(Temp):
    '''
    Returns a RGBA color value from 0..1 
    '''
    MAXTEMP = 10
    MINTEMP = 1

    if Temp >= MAXTEMP:
        colorValue = 1
    elif Temp <= MINTEMP:
        colorValue = 0
    else:
        colorValue = (MAXTEMP - Temp) / (MAXTEMP - MINTEMP)
    return colorValue    

def plotLatLonColor(myCoord, ChunkNo):
    '''
    Splits the coordinates into chucks and returns 
    variables ready for ploting with ie. matplotlib
    '''
    lon, lat = convSpherCoordTo2D(myCoord)
    NoEntries = len(lon)
    CoorDistance = int(NoEntries / ChunkNo)
    ColorArray =[]

    for ent in range(NoEntries):
        if ent % CoorDistance == 0:
            # print(myCoordinates[ent,1])
            # print(myCoordinates[ent,0])
            coordTemp = minWeatherAtLocation(myCoord[ent,1], myCoord[ent,0])
            RGBvalue = colorCodeTemperature(coordTemp)
            # print(myCoordinates[ent], RGBvalue)

        ColorArray.append(RGBvalue)

    
    return lon, lat, ColorArray



myCoordinates = getCoordinates(myORIGIN,myDESTINATION)
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

