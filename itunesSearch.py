import requests
import json
import pandas as pd
import numpy as np

def search_pod(key_word, cursor):
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
    res = res[0]

    itunes_id = res['collectionId']
    query = """
    SELECT titles, descriptions, genre, subgenre, artwork_url
    FROM all_pods
    WHERE itunes_id = %s;"""
    cursor.execute(query, (str(itunes_id), ))
    match = cursor.fetchone()

    pod = {"id":itunes_id,
            "title":match[0],
            "description":match[1],
            "genre":match[2],
            "subgenre":match[3],
            "artwork":match[4]}
    return pod

def get_recommendations(pod, cursor):
    itunes_id = pod["id"]
    print(itunes_id)
    query = \
    """SELECT match_id, score
    FROM all_matches_meanvec
    WHERE itunes_id = %s
    ORDER BY score DESC;"""
    cursor.execute(query, (str(itunes_id), ))
    res = cursor.fetchall()
    match_ids = [str(r[0]) for r in res]
    scores = {str(r[0]):r[1] for r in res}

    query = """
    SELECT itunes_id, titles, descriptions, genre, subgenre, artwork_url
    FROM all_pods
    WHERE itunes_id IN %s;"""
    cursor.execute(query, (tuple(match_ids),))
    matches = cursor.fetchall()

    results = [{"itunes_id": str(m[0]),
                "title": m[1],
                "description": m[2],
                "genre": m[3],
                "subgenre": m[4],
                "artwork_url": m[5].replace("600x600","100x100")}
                for i, m in enumerate(matches)]
    sc = np.zeros(len(scores))
    for i, r in enumerate(results):
        r["similarity"] = scores[r["itunes_id"]]
        sc[i] = scores[r["itunes_id"]]
    idx = np.argsort(sc)[::-1]
    temp = []
    for i in idx:
        temp.append(results[i])
    results = temp

    # title = []
    # description = []
    # genre = []
    # subgenre = []
    # artwork_url = []
    # for m in matches:
    #     title.append(m[0])
    #     description.append(m[1])
    #     genre.append(m[2])
    #     subgenre.append(m[3])
    #     artwork_url.append(m[4])
    # results = pd.DataFrame({"itunes_id":match_ids,
    #     "title":title, "description":description,
    #     "genre":genre, "subgenre":subgenre,
    #     "artwork_url":artwork_url,
    #     "similarity":scores})
    return results
