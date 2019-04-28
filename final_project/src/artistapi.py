
import requests
import json

def getArtistLocation(artist):
    """Given a artist/band name [string], function returns a location [string]"""

    req = 'https://musicbrainz.org/ws/2/artist?query="{0}"&fmt=json'.format(artist) 
  
    r = requests.get(req)

    content = r.content

    candidateArtists = json.loads(content)
    try:
        artist = candidateArtists["artists"][0] #Assuming max score is best fit (not the best)

        location = artist['begin-area']['name'].encode('utf8')
    except:
        location = "Couldn't find"

    return location

testArtist = 'beat connection'

location = getArtistLocation(testArtist)
assert location == "Seattle", "Bad Request"
print("Validated")



