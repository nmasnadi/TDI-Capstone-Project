import requests
import json
import pandas as pd
import numpy as np

def search_pod_by_id(itunes_id, cursor):
    query = """
    SELECT titles, descriptions, genre, subgenre, artwork_url
    FROM all_pods
    WHERE itunes_id = %s;"""
    cursor.execute(query, (str(itunes_id), ))
    match = cursor.fetchone()

    pod = {"itunes_id":itunes_id,
            "title":match[0],
            "description":match[1],
            "genre":match[2],
            "subgenre":match[3],
            "artwork_url":match[4]}
    return pod

def search_pod_by_keyword(key_word, cursor):

    itunesUrl = "https://itunes.apple.com/search?entity=podcast&attribute=titleTerm&term="
    testUrl = itunesUrl + key_word
    r = requests.get(testUrl)
    res = json.loads(r.text)['results']

    if not res:
        return []

    itunes_ids = [str(r['collectionId']) for r in res]

    query = """
    SELECT itunes_id, titles, descriptions, genre, subgenre, artwork_url
    FROM all_pods
    WHERE itunes_id IN %s;"""
    cursor.execute(query, (tuple(itunes_ids),))
    matches = cursor.fetchall()

    pods = [{"itunes_id": str(m[0]),
                "title": m[1],
                "description": m[2],
                "genre": m[3],
                "subgenre": m[4],
                "artwork_url": m[5].replace("600x600","100x100")}
                for i, m in enumerate(matches)]

    match_ids = [str(m[0]) for m in matches]
    pods2 = []
    for _id in itunes_ids:
        if _id in match_ids:
            idx = match_ids.index(_id)
            pods2.append(pods[idx])

    return pods2

def get_recommendations(pod, cursor):
    itunes_id = pod["itunes_id"]
    query = \
    """SELECT match_id, score
    FROM all_matches_meanvec
    WHERE itunes_id = %s;"""
    cursor.execute(query, (str(itunes_id), ))
    res = cursor.fetchone()
    match_ids = res[0].split(',')
    scores_temp = res[1].split(',')
    scores = dict()
    for m, s in zip(match_ids, scores_temp):
        scores[m] = s

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
                "subgenre": m[4]}
                for m in matches]

    for i, m in enumerate(matches):
        try:
            results[i]["artwork_url"] = m[5].replace("600x600","100x100")
        except:
            results[i]["artwork_url"] = None

    sc = np.zeros(len(scores))
    for i, r in enumerate(results):
        r["similarity"] = scores[r["itunes_id"]]
        sc[i] = scores[r["itunes_id"]]
    idx = np.argsort(sc)[::-1]
    return [results[i] for i in idx]

def get_plotting_data(cursor):
    query = "SELECT titles, genre, subgenre, x_tsne, y_tsne, color, artwork_url, itunes_id FROM all_pods;"
    cursor.execute(query)
    res = cursor.fetchall()
    titles = [r[0] for r in res]
    genre = [r[1] for r in res]
    subgenre = [r[2] for r in res]
    x_tsne = [r[3] for r in res]
    y_tsne = [r[4] for r in res]
    color = [r[5] for r in res]
    artwork_url = [r[6] for r in res]
    itunes_id = [r[7] for r in res]
    plot_data = pd.DataFrame({"titles":titles, "genre":genre,\
                 "subgenre":subgenre, "x":x_tsne, \
                 "y":y_tsne, "color":color, \
                 "artwork_url":artwork_url, \
                 "itunes_id":itunes_id})
    def smaller(x):
        if x:
            return x.replace("600x600","100x100")
        else:
            return None
    plot_data["artwork_url"] = plot_data["artwork_url"].apply(smaller)
    return plot_data

def random_pod(cursor):
    query = "SELECT titles FROM all_pods ORDER BY RANDOM() LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()[0]
