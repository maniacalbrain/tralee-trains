import re
import urllib
import webbrowser
from xml.etree.ElementTree import parse

#Get data from Irish Rail website
u = urllib.urlopen('http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML')

xmlns = '{http://api.irishrail.ie/realtime/}'
train_dict = {}

doc = parse(u)
for train in doc.iter():
    for item in train.findall(xmlns + 'PublicMessage'):
         #if Tralee is contained in the PublicMessage to train is either traveling to or from there
        if 'Tralee' in item.text.split():
            #add nested dictionary to train_dict. 
            train_dict[train.find(xmlns + 'TrainCode').text] = {'Latitude' : train.find(xmlns + 'TrainLatitude').text,
            'Longitude' : train.find(xmlns + 'TrainLongitude').text,
            'Direction' : train.find(xmlns + 'Direction').text,
            'Route' : re.search(r'(\w*)\sto\s(\w*)(\s)?(\w*)?', train.find(xmlns + 'PublicMessage').text).group()}

print train_dict
            
map_string = "https://maps.googleapis.com/maps/api/staticmap?center=Athlone&zoom=7&size=700x600&maptype=roadmap"
color = 'blue'
for i in train_dict:
    #if train is traveling towards Tralee change color to green, else blue will be used.
    if 'Tralee' in str(train_dict[i]['Direction']).split():
        color = 'green'
    map_string += "&markers=color:" + color + "%7Clabel:" + str(i) + "%7C" + str(train_dict[i]['Latitude']) + ",%20" + (train_dict[i]['Longitude'])

webbrowser.open(map_string)
