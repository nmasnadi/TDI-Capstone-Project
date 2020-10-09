from psycopg2 import connect, sql
import os
import requests
import json
import pandas as pd
import numpy as np

class SqlTable:
    def __init__(self, local = True):
        if local:
            conn = connect(dbname="podcasts", user="naeem", password="mypass", host="localhost", port="5432")
        else:
            conn = connect(os.environ['DATABASE_URL'], sslmode='require')
        self.cursor = conn.cursor()
        self.plot_data = self.get_plotting_data()

    def pod_lookup(self, itunes_ids):

        query = """
        SELECT itunes_id, titles, descriptions, genre, subgenre, artwork_url
        FROM all_pods
        WHERE itunes_id in ({});"""
        self.cursor.execute(sql.SQL(query).format(sql.SQL(', ').join(map(sql.Literal, itunes_ids))))
        match = self.cursor.fetchall()
        df = pd.DataFrame(match, columns = ["itunes_id", "title", "description", "genre", "subgenre", "artwork_url"])
        return df

    def search_pod_by_keyword(self, key_word):
        itunes_url = "https://itunes.apple.com/search?entity=podcast&attribute=titleTerm&term="
        testUrl = itunes_url + key_word
        r = requests.get(testUrl)
        res = json.loads(r.text)['results']

        if not res:
            return []

        itunes_ids = [str(r['collectionId']) for r in res]

        query = """
        SELECT itunes_id, titles, descriptions, genre, subgenre, artwork_url
        FROM all_pods
        WHERE itunes_id IN ({});"""
        self.cursor.execute(sql.SQL(query).format(sql.SQL(', ').join(map(sql.Literal, itunes_ids))))
        matches = self.cursor.fetchall()
        df = pd.DataFrame(matches, columns = ["itunes_id", "title", "description", "genre", "subgenre", "artwork_url"])

        idx = []
        for _id in df["itunes_id"]:
            idx.append(itunes_ids.index(_id))
        idx = np.argsort(np.array(idx))
        df = df.loc[idx].reset_index(drop=True)

        return df

    def get_recommendations(self, itunes_id):

        query = """
        SELECT match_id, score
        FROM all_matches_meanvec
        WHERE itunes_id = {_id};"""
        self.cursor.execute(sql.SQL(query).format(_id = sql.Literal(itunes_id)))
        res = self.cursor.fetchone()
        match_ids = res[0].split(',')
        scores = res[1].split(',')
        scores_df = pd.DataFrame({"itunes_id":match_ids, "score":scores})
        recommendations_df = self.pod_lookup(match_ids)
        return scores_df.merge(recommendations_df, on = "itunes_id")

    def get_plotting_data(self):
        query = """
        SELECT titles, genre, subgenre, x_tsne, y_tsne, itunes_id
        FROM all_pods;"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        df = pd.DataFrame(res, columns = \
            ["title", "genre", "subgenre", "x", "y", "itunes_id"])
        return df

    def random_pod(self, N = 1):
        query = "SELECT itunes_id FROM all_pods ORDER BY RANDOM() LIMIT {}"
        self.cursor.execute(sql.SQL(query).format(sql.Literal(N)))
        itunes_ids = self.cursor.fetchall()
        itunes_ids = [_id[0] for _id in itunes_ids]
        return self.pod_lookup(itunes_ids)
