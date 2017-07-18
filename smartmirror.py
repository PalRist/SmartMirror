#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import datetime as dt
import os
import platform
from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale_linux = 'nb_NO.UTF8'
ui_locale_macOS = 'nb_NO'
if (platform.system()).lower() == 'darmin':
    ui_locale = ui_locale_macOS
else:
    ui_locale = ui_locale_linux
time_format = 24 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
news_country_code = 'no_no'
weather_api_token = '05e9697d6d051b6c5073f673544b5418' # create account at https://darksky.net/dev/
weather_lang = 'nb' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
ThisDate = dt.datetime.now().replace(microsecond=0).isoformat()
TempThreshold = 1


@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': os.path.join("imgs", "weather_icons", "Sun.png"),  # clear sky day
    'wind': os.path.join("imgs", "weather_icons", "Wind.png"),   #wind
    'cloudy': os.path.join("imgs", "weather_icons", "Cloud.png"),  # cloudy day
    'partly-cloudy-day': os.path.join("imgs", "weather_icons", "PartlySunny.png"),  # partly cloudy day
    'rain': os.path.join("imgs", "weather_icons", "Rain.png"),  # rain day
    'snow': os.path.join("imgs", "weather_icons", "Snow.png"),  # snow day
    'snow-thin': os.path.join("imgs", "weather_icons", "Snow.png"),  # sleet day
    'fog': os.path.join("imgs", "weather_icons", "Haze.png"),  # fog day
    'clear-night': os.path.join("imgs", "weather_icons", "Moon.png"),  # clear sky night
    'partly-cloudy-night': os.path.join("imgs", "weather_icons", "PartlyMoon.png"),  # scattered clouds night
    'thunderstorm': os.path.join("imgs", "weather_icons", "Storm.png"),  # thunderstorm
    'tornado': os.path.join("imgs", "weather_icons", "Tornado.png"),    # tornado
    'hail': os.path.join("imgs", "weather_icons", "Hail.png")  # hail
}

class TravelMap(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.image = Image.open(os.path.join(os.path.join("imgs", "Vestlandskart","ActiveRoad.png")))
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
        self.tempImg = Image.open(os.path.join("imgs","Vestlandskart", "road_trans.png"))
        
        # print(MinTempForde)

        if MinTempForde <= TempThreshold:
            self.imgForde = Image.open(os.path.join(("imgs","Vestlandskart","forde.png")))
            self.tempImg.paste(self.imgForde, (0, 0), self.imgForde)
            # self.tempImg.save('assets/ActiveRoad2.png')

        if MinTempSande <= TempThreshold:
            self.imgSande = Image.open(os.path.join("imgs","Vestlandskart", "sande.png"))
            self.tempImg.paste(self.imgSande, (0, 0), self.imgSande)

        if MinTempVadheim <= TempThreshold:
            self.imgVadheim = Image.open(os.path.join("imgs","Vestlandskart", "vadheim.png"))
            self.tempImg.paste(self.imgVadheim, (0, 0), self.imgVadheim)

        if MinTempHoyanger <= TempThreshold:
            self.imgHoyanger = Image.open(os.path.join("imgs","Vestlandskart", "hoyanger.png'"))
            self.tempImg.paste(self.imgHoyanger, (0, 0), self.imgHoyanger)

        self.tempImg = self.tempImg.resize((140, 231), Image.BICUBIC) #125, 216
        self.tempImg.save(os.path.join("imgs","Vestlandskart", "ActiveRoad.png"))

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


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print "Error: %s. Cannot get weather." % e

        self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Nyheter' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "https://news.google.com/news?ned=no_no&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print "Error: %s. Cannot get news." % e

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open(os.path.join("assets", "Newspaper.png"))
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)


class Calendar(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.title = 'Calendar Events'
        self.calendarLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.calendarLbl.pack(side=TOP, anchor=E)
        self.calendarEventContainer = Frame(self, bg='black')
        self.calendarEventContainer.pack(side=TOP, anchor=E)
        self.get_events()

    def get_events(self):
        #TODO: implement this method
        # reference https://developers.google.com/google-apps/calendar/quickstart/python

        # remove all children
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()

        calendar_event = CalendarEvent(self.calendarEventContainer)
        calendar_event.pack(side=TOP, anchor=E)
        pass


class CalendarEvent(Frame):
    def __init__(self, parent, event_name="Event 1"):
        Frame.__init__(self, parent, bg='black')
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=TOP, anchor=E)

class SpotifyToggle(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.parent = parent
        self.label = None
        self.doUpdate()

    def resize_image(self):
        '''
        resizing image accordfing to width / height
        Keeping the aspect ratio and just using the shortest of width / height to adjust the image
        :return:
        '''

        if self.label is not None:
            self.label.pack_forget()
        self.image = Image.open(os.path.join("imgs", "spotify", "logo_large_white.png"))
        self.image = self.image.convert('RGB')
        smallest = min(self.width, self.height)
        size = float(smallest / 5.0)
        self.image = self.image.resize((smallest, smallest), Image.BICUBIC) #125, 216
        self.photo = ImageTk.PhotoImage(self.image)
        self.arc = Canvas(self.parent, width=200, height=200).create_arc(0,smallest,smallest,0, fill="blue", outline="#DDD", width=4)


        self.label = Label(image=self.photo, borderwidth=0, state='normal')


        self.label.image = self.photo

        self.label.pack(side=RIGHT, anchor=E, padx=100)


    def doUpdate(self):
        self.after(1000, self.doUpdate)
        self.width, self.height = self.parent.winfo_width(), self.parent.winfo_height()
        self.resize_image()





class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()

        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')

        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)

        # news
        # self.news = News(self.bottomFrame)
        # self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)
        # calender - removing for now
        # self.calender = Calendar(self.bottomFrame)
        # self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)
        # travel map
        self.screen_width =  self.tk.winfo_width()
        self.screen_height = self.tk.winfo_height()
        self.map = TravelMap(self.bottomFrame)
        self.map.pack(side = LEFT, anchor=S, padx=100, pady=60)
        self.spotify = SpotifyToggle(self.bottomFrame)
        self.map.pack(side = RIGHT, anchor=S, padx=100, pady=60)



    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
