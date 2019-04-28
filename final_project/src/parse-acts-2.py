import artistapi as Artist
import xml.etree.ElementTree as ET
import os
import sys
import datetime
import csv  
from datetime import date

nprRssFeed = os.path.normpath("C:/Users/tmoran/Desktop/msga580/final_project/data/npr-acts.xml")
output_folder = r'C:\Users\tmoran\Desktop'
output_csv = 'npr_artists'

def todays_date():
    """Returns a string representation of today's date"""
    todaydate = str(date.today())
    return todaydate

def getDateTime():
    #Gets current date which is in turn used to define unique model run (suitable for file names)
    now = datetime.datetime.now()
    datetimeString = str(now.strftime("%Y%m%d_%H%M%S"))
    return datetimeString

def write_data(csv_writer, npr_artist):
	csv_writer.writerow(npr_artist)

root = ET.parse(nprRssFeed).getroot()[0]

datetime_string = getDateTime()

csv_fields = [ 
    'title',
    "description",
    "location",
    "pubDate", 
    "guid",
    "imgLink", 
    "actURL"
]

csv_filename = os.path.join(output_folder, output_csv + "_" + datetime_string + ".csv")
csvfile = open(csv_filename, 'wb')
npr_csv = csv.DictWriter(csvfile, fieldnames = csv_fields) #Instantiates CSV DictWriter Object
npr_csv.writeheader() #Writes header per 'csv_fields' list


for currentAct in root.findall('item'):
    try: 
        currentNPRAct = {}

        for item in currentAct._children: 
            if item.tag == "title":
                act = str(item.text.encode('utf-8').strip())
                currentNPRAct['title'] = act
                artistLocation = Artist.getArtistLocation(act)
                currentNPRAct['location'] = artistLocation
            if item.tag == "description": 
                description = str(item.text.encode('utf-8').strip())
                currentNPRAct['description'] = description
            if item.tag == "pubDate":
                pubDate = str(item.text.encode('utf-8').strip())
                currentNPRAct['pubDate'] = pubDate
            if item.tag == "guid":
                guid = str(item.text.encode('utf-8').strip())
                currentNPRAct['guid'] = guid
            if item.tag == "{http://www.itunes.com/dtds/podcast-1.0.dtd}image":
                imgLink = str(item.attrib['href'].encode('utf-8').strip())
                currentNPRAct['imgLink'] = imgLink
            if item.tag == "enclosure":
                actLink = str(item.attrib["url"].encode('utf-8').strip())
                currentNPRAct['actURL'] = actLink
                
        write_data(npr_csv, currentNPRAct)    
        # print "{0} * {1} * {2} * {3} * {4} * {5}".format(act, description, pubDate, guid, imgLink, actLink) 
        

    except Exception as e: 
        print act
        print e
