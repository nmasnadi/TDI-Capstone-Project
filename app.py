from flask import Flask, render_template, request, redirect, url_for
from itunesSearch import search_pod
from bokeh.embed import components
from bokeh.resources import CDN

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
    f = open("clusters.html", "r")
    cluster_plot = f.read()

    return render_template("results.html", cluster_plot = cluster_plot, \
    pod = pods[0], \
    resources = CDN.render())

if __name__ == '__main__':
    app.run(port=33507)
