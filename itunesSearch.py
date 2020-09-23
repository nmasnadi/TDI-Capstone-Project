import requests
import json
import pandas as pd
import numpy as np

def search_pod(key_word, cursor, itunes_id = None):
    if itunes_id == None:
        itunesUrl = "https://itunes.apple.com/search?entity=podcast&attribute=titleTerm&term="
        testUrl = itunesUrl + key_word
        r = requests.get(testUrl)
        res = json.loads(r.text)['results'][0]
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
                "subgenre": m[4],
                "artwork_url": m[5].replace("600x600","100x100")}
                for i, m in enumerate(matches)]
    sc = np.zeros(len(scores))
    for i, r in enumerate(results):
        r["similarity"] = scores[r["itunes_id"]]
        sc[i] = scores[r["itunes_id"]]
    idx = np.argsort(sc)[::-1]
    return [results[i] for i in idx]

def get_plotting_data(cursor):
    query = "SELECT titles, genre, subgenre, x_tsne, y_tsne, color FROM all_pods;"
    cursor.execute(query)
    res = cursor.fetchall()
    titles = [r[0] for r in res]
    genre = [r[1] for r in res]
    subgenre = [r[2] for r in res]
    x_tsne = [r[3] for r in res]
    y_tsne = [r[4] for r in res]
    color = [r[5] for r in res]
    plot_data = pd.DataFrame({"titles":titles, "genre":genre,\
                 "subgenre":subgenre, "x":x_tsne, \
                 "y":y_tsne, "color":color})
    return plot_data

def random_pod(cursor):
    query = "SELECT titles FROM all_pods ORDER BY RANDOM() LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()[0]
