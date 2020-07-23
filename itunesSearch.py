# import urllib.parse
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
    testUrl = itunesUrl + key_word #urllib.parse.quote(key_word)
    r = requests.get(testUrl)
    res = json.loads(r.text)['results'][0]
    return res['collectionName'], res['artworkUrl60']
