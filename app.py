from flask import Flask, render_template, request, redirect, url_for
# from bokeh.embed import components
from bokeh.resources import CDN
from itunesSearch import search_pod, get_recommendations, get_plotting_data
from psycopg2 import connect
from makePlots import make_cluster_plot
# from random import randrange

# conn = connect(dbname="podcasts", user="naeem", password="mypass", host="localhost", port="5432")
import os
DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()
pod_placeholders = ["Serial", "This American Life", \
    "Dr. Death", "Radiolab", "The Daily", \
    "Stuff You Should Know", "Planet Money from NPR", \
    "POD Save America", "NBA Hang Time", "Up First"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key_word = request.form['pod_name']
        return redirect(url_for('show_results_id', search_term = key_word))
    else:
        query = "SELECT titles FROM all_pods ORDER BY RANDOM() LIMIT 1"
        cursor.execute(query)
        pod_placeholder = cursor.fetchone()[0]
        print(pod_placeholder)
        # idx = randrange(len(pod_placeholders))
        return render_template("index.html", pod_placeholder = pod_placeholder)

@app.route('/term=<search_term>', methods=['GET', 'POST'])
@app.route('/itunes_id=<itunes_id>&offset=<offset>', methods=['GET', 'POST'])
def show_results_id(search_term = None, itunes_id = None, offset = 0):
    offset = int(offset)
    pod = search_pod(search_term, cursor, itunes_id)
    recs = get_recommendations(pod, cursor)
    genre_show_list = [r['genre'] for r in recs[offset:offset+10]]
    plot_data = get_plotting_data(cursor)
    cluster_plot = make_cluster_plot(plot_data, genre_show_list)
    return render_template("results.html", cluster_plot = cluster_plot, \
    pod = pod, \
    pod_recommendations = recs, \
    offset = offset, \
    resources = CDN.render())

if __name__ == '__main__':
    app.run(port=33507)
