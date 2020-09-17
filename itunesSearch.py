import requests
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

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
    itunes_ids = [r['collectionId'] for r in res]
    # itunes_titles = [r['collectionName'] for r in res]
    # itunes_artwork = [r['artworkUrl600'] for r in res]
    base_url = "https://podcasts.apple.com/podcast/id"
    itunes_descriptions = []
    for _id in itunes_ids:
        url = base_url + str(_id)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="lxml")
        description = soup.find('section', \
            attrs={"class":"product-hero-desc__section"}).text
        itunes_descriptions.append(" ".join(description.split()))

    for i in range(len(pods)):
        pods[i]['description'] = itunes_descriptions[i]
    # return itunes_ids, itunes_titles, itunes_descriptions, itunes_artwork
    return pods

# def get_recommendations(search_term, n_rec = 10):
#     itunes_ids, itunes_titles, \
#         itunes_descriptions, itunes_artwork = search_pod(search_term)
#     pods_mean_vec = pd.read_pickle("pods_mean_vec_description.pkl")
#     vecs = pods_mean_vec['vector'].to_numpy()
#     vecs = np.array([vec for vec in vecs])
#     sims = cosine_similarity(vecs)
#
#     for i in range(len(itunes_ids)):
#         try:
#             pod_idx = pods_mean_vec[pods_mean_vec["itunes_id"] == itunes_ids[i]].index[0]
#             pod_itunes_id = itunes_ids[i]
#             pod_title = itunes_titles[i]
#             pod_artwork = itunes_artwork[i]
#             break
#         except:
#             pass
#
#     idx = np.argsort(sims[pod_idx])[::-1][1:n_rec+1]
#     similarity = sims[pod_idx][idx]
#     result_pd = pods_mean_vec.loc[idx,["itunes_id", "titles", "descriptions",
#         "genre", "subgenre"]].reset_index(drop=True)
#     recommendations = []
#     for i in range(result_pd.shape[0]):
#         _id = result_pd.loc[i, "itunes_id"]
#         title = result_pd.loc[i, "titles"]
#         desc = result_pd.loc[i, "descriptions"]
#         genre = result_pd.loc[i, "genre"]
#         subgenre = result_pd.loc[i, "subgenre"]
#         recommendations.append({'id':_id, 'title':title, 'description': desc,
#                                 'genre':genre, 'subgenre':subgenre,
#                                 'similarity':similarity[i]})
#     podcast = {'id':pod_itunes_id, 'title':pod_title, 'artwork': pod_artwork}
#     return podcast, recommendations
