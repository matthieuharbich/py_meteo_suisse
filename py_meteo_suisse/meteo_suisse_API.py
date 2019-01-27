#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup


def get_location_id(city):
    first_two_char = city[:2]
    search_url = "https://www.meteosuisse.admin.ch/etc/designs/meteoswiss/ajax/search/"+first_two_char+".json"
    result = requests.get(search_url).json()
    for i in result:
        if i.split(';')[5].lower() == city.lower():
            location_id = i.split(';')[0]
    return location_id

def get_last_file_data():
    url = "https://www.meteosuisse.admin.ch/home.html?tab=overview"
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    temp = soup.find('div', attrs={'class': 'overview__local-forecast clearfix'})['data-json-url'].split('/')[-3].split('_')
    time = temp[-1]
    date = temp[-2]
    return time, date

def get_weather_json_url(city):
    location_id = get_location_id(city)
    time, date = get_last_file_data()
    url = "https://www.meteosuisse.admin.ch/product/output/forecast-chart/version__"+date+"_"+time+"/fr/"+location_id+".json"
    return url

def get_weather_json(city):
    url = get_weather_json_url(city)
    response = requests.get(url).json()
    return response


    