import requests
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# from bs4 import BeautifulSoup

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
    pods = [{"id":r['collectionId'],
            "title":r['collectionName'],
            "artwork":r['artworkUrl600']} for r in res]
    # itunes_ids = [r['collectionId'] for r in res]
    # # itunes_titles = [r['collectionName'] for r in res]
    # # itunes_artwork = [r['artworkUrl600'] for r in res]
    # base_url = "https://podcasts.apple.com/podcast/id"
    # itunes_descriptions = []
    # for _id in itunes_ids:
    #     url = base_url + str(_id)
    #     req = requests.get(url)
    #     soup = BeautifulSoup(req.text, features="lxml")
    #     description = soup.find('section', \
    #         attrs={"class":"product-hero-desc__section"}).text
    #     itunes_descriptions.append(" ".join(description.split()))
    #
    # for i in range(len(pods)):
    #     pods[i]['description'] = itunes_descriptions[i]
    return pods
