import requests
import json

def search_pod(key_word):
    itunesUrl = 'https://itunes.apple.com/search?'
    parameters = {}
    parameters['entity'] = 'podcast'
    parameters['attribute'] = 'titleTerm'

    requestString = ''
    for param in parameters:
        paramString = param + '=' + parameters[param]
        if len(requestString) == 0:
            requestString = paramString
        else:
            requestString = requestString + '&' + paramString

    itunesUrl = itunesUrl + requestString + '&term='
    testUrl = itunesUrl + key_word
    r = requests.get(testUrl)
    res = json.loads(r.text)['results']
    itunes_ids = [r['collectionId'] for r in res]
    itunes_titles = [r['collectionName'] for r in res]
    itunes_artwork = [r['artworkUrl600'] for r in res]
    return itunes_ids, itunes_titles, itunes_artwork
