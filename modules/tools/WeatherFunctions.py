import requests
import json
import feedparser
import datetime as dt



# class Weather():
weather_api_token = '05e9697d6d051b6c5073f673544b5418' # create account at https://darksky.net/dev/
weather_latg = 'nb' # see https://darksky.net/dev/docs/forecast for full list of latguage parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
ThisDate = dt.datetime.now().replace(microsecond=0).isoformat()
TempThreshold = 1

def minWeatherAtLocation(latitude, longitude):
    weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s,%s?exclude=currently,flags&latg=%s&units=%s" % (weather_api_token, latitude, longitude, ThisDate, weather_latg, weather_unit)
    # print(weather_req_url) 
    r = requests.get( weather_req_url )
    weather_obj = json.loads(r.text)
    ThisHour = dt.datetime.now().hour
    ColdestTemp = 100
    # ColdestHour = 25

    for hour in range(24):
        if hour <= ThisHour:
            temperature = float(weather_obj['hourly']['data'][hour]['temperature'])
            if temperature <= ColdestTemp:
                ColdestTemp = temperature
                # ColdestHour = hour
    return ColdestTemp#, ColdestHour