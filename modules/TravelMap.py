from Tkinter import *
import time
import requests
import json
import feedparser
import datetime as dt

from PIL import Image, ImageTk

news_country_code = 'no_no'
weather_api_token = '05e9697d6d051b6c5073f673544b5418' # create account at https://darksky.net/dev/
weather_lang = 'nb' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
ThisDate = dt.datetime.now().replace(microsecond=0).isoformat()
TempThreshold = 1


class TravelMap(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.image = Image.open('assets/ActiveRoad.png')
        self.image = self.image.convert('RGB')
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = Label(image=self.photo, borderwidth=0, state='normal')
        self.label.image = self.photo 
        self.label.pack(side=LEFT, anchor=E, padx=100)
        self.doUpdate()

    def doUpdate(self):
        self.MinTempForde = float(self.minWeatherAtLocation(61.4518,5.82))
        self.MinTempSande = float(self.minWeatherAtLocation(61.3251,5.7977))
        self.MinTempVadheim = float(self.minWeatherAtLocation(61.2088,5.8235))
        self.MinTempHoyanger = float(self.minWeatherAtLocation(61.2176,6.0638))
        self.makeRoad(self.MinTempForde, self.MinTempSande, self.MinTempVadheim, self.MinTempHoyanger)
        self.after(60000, self.doUpdate)

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
        # print('Minstetemperatur i Forde %s i dag klokken %s.' % (MinTempForde[0], MinTempForde[1]))

    def makeRoad(self, MinTempForde, MinTempSande, MinTempVadheim, MinTempHoyanger):
        self.tempImg = Image.open('assets/road_trans.png')
        
        # print(MinTempForde)

        if MinTempForde <= TempThreshold:
            self.imgForde = Image.open('assets/forde.png')
            self.tempImg.paste(self.imgForde, (0, 0), self.imgForde)
            # self.tempImg.save('assets/ActiveRoad2.png')

        if MinTempSande <= TempThreshold:
            self.imgSande = Image.open('assets/sande.png')
            self.tempImg.paste(self.imgSande, (0, 0), self.imgSande)

        if MinTempVadheim <= TempThreshold:
            self.imgVadheim = Image.open('assets/vadheim.png')
            self.tempImg.paste(self.imgVadheim, (0, 0), self.imgVadheim)

        if MinTempHoyanger <= TempThreshold:
            self.imgHoyanger = Image.open('assets/hoyanger.png')
            self.tempImg.paste(self.imgHoyanger, (0, 0), self.imgHoyanger)

        self.tempImg = self.tempImg.resize((140, 231), Image.BICUBIC) #125, 216
        self.tempImg.save('assets/ActiveRoad.png')

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

