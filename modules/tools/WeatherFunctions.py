import requests
import json
import feedparser
import datetime as dt

weather_api_token = '05e9697d6d051b6c5073f673544b5418' # create account at https://darksky.net/dev/
weather_lang = 'nb' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
ThisDate = dt.datetime.now().replace(microsecond=0).isoformat()
TempThreshold = 1

class Weather():
    def minWeatherAtLocation(self, latitude, longitude):
    weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s,%s?exclude=currently,flags&lang=%s&units=%s" % (weather_api_token, latitude, longitude, ThisDate, weather_lang, weather_unit)

    r = requests.get( weather_req_url )
    weather_obj = json.loads(r.text)
    ThisHour = dt.datetime.now().hour
    # degree_sign = u'\N{DEGREE SIGN}'
    self.ColdestTemp = 50
    self.ColdestHour = 25

    for hour in range(24):
        if hour <= ThisHour:
            self.temperature = float(weather_obj['hourly']['data'][hour]['temperature'])
            if self.temperature <= self.ColdestTemp:
                self.ColdestTemp = self.temperature
                self.ColdestHour = hour

    # temperatureMin = "%s%s" % (str(ColdestTemp), degree_sign)
    return self.ColdestTemp#, self.ColdestHour