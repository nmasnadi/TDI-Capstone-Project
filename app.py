from flask import Flask, render_template, request, redirect, url_for
from itunesSearch import search_pod
from plotting import cluster_plot
from bokeh.plotting import show
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd

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
    # itunes_ids, itunes_titles, itunes_artwork = search_pod(search_term)
    # print(itunes_titles[0] + ": " + str(itunes_ids[0]))
    # clusters = cluster_plot()
    # script, div = components(clusters)

    # pods_mean_vec = pd.read_pickle("pods_mean_vec_description.pkl")
    # t = pods_mean_vec[["titles", "descriptions", "genre", "subgenre"]][:10]
    # return render_template("results.html", script = t.to_html())
    f = open("clusters.html", "r")
    cluster_plot = f.read()
    return render_template("results.html", cluster_plot = cluster_plot, \
    resources = CDN.render())

if __name__ == '__main__':
    app.run(port=33507)
