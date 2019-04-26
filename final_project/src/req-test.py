
import requests
import xml.etree.ElementTree as ET
import json

#use this to attribute csv with location in name and x,y and group type


currentAct = "beat%20connection"

req = 'https://musicbrainz.org/ws/2/artist?query="{0}"&fmt=json'.format(currentAct) 
#use this to do related acts (on demand api call)
# get top 5 candidates, create object with band name, type, location
# get location and bind to object, those with no location drop
# add graphics to new layer
# zoom to extent of these 

r = requests.get(req)

content = r.content

candidateArtists = json.loads(content)

artist = candidateArtists["artists"][0] #Assuming max score is best fit (not the best)

location = artist['begin-area']['name'].encode('utf8')

print location









'''

root = ET.fromstring(content)

artistScore = root._children[0]._children[0].attrib['{http://musicbrainz.org/ns/ext#-2.0}score']
artist = root._children[0]._children[0][0]

artist_properties = root._children[0]._children[0]._children

for artistProperty in artist_properties:
    if artistProperty.tag == '{http://musicbrainz.org/ns/mmd-2.0#}begin-area': 
        location_properties = artistProperty._children
        for prop in location_properties:
            print prop.tag

'''



