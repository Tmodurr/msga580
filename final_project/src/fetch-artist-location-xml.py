'''xml remnants before I ported over to json api - xml is nasty'''
import xml.etree.ElementTree as ET

root = ET.fromstring(content)

artistScore = root._children[0]._children[0].attrib['{http://musicbrainz.org/ns/ext#-2.0}score']
artist = root._children[0]._children[0][0]

artist_properties = root._children[0]._children[0]._children

for artistProperty in artist_properties:
    if artistProperty.tag == '{http://musicbrainz.org/ns/mmd-2.0#}begin-area': 
        location_properties = artistProperty._children
        for prop in location_properties:
            print prop.tag
