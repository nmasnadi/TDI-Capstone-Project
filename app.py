from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.resources import CDN
from itunesSearch import search_pod, get_recommendations
from psycopg2 import connect

# conn = connect(dbname="podcasts", user="naeem", password="mypass", host="localhost", port="5432")

import os
DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')
# conn = connect(dbname="podcasts", user="naeem", password="mypass", host="localhost", port="5432")
cursor = conn.cursor()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key_word = request.form['pod_name']
        return redirect(url_for('show_results', search_term = key_word))
    else:
        return render_template("index.html")

@app.route('/results/<search_term>', methods=['GET', 'POST'])
def show_results(search_term):
    pods = search_pod(search_term)
    recs = get_recommendations(pods[0], cursor)
    f = open("clusters.html", "r")
    cluster_plot = f.read()
    return render_template("results.html", cluster_plot = cluster_plot, \
    pod = pods[0], \
    pod_recommendations = recs[:10], \
    resources = CDN.render())

if __name__ == '__main__':
    app.run(port=33507)
