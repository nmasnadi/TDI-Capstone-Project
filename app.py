from flask import Flask, render_template, request, redirect, url_for
from searchDatabase import SqlTable
from bokehPlot import make_cluster_plot
import random

db = SqlTable(local = True)
pod_placeholders = ["Serial", "This American Life", \
    "Dr. Death", "Radiolab", "The Daily", \
    "Stuff You Should Know", "Planet Money from NPR", \
    "POD Save America", "NBA Hang Time", "Up First"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key_word = request.form['pod_name']
        if not key_word:
            key_word = "random_podcast"
        return redirect(url_for('show_search_results', \
            search_term = key_word, offset = 0))
    else:
        return render_template("index.html", \
            pod_placeholder = random.choice(pod_placeholders))

@app.route('/term=<search_term>&offset=<offset>', methods=['GET', 'POST'])
def show_search_results(search_term, offset = 0):
    offset = int(offset)
    if search_term == "random_podcast":
        pods = db.random_pod()
        search_term = pods["title"]
        table_title = "Random Suggestion"
    else:
        table_title = 'Search Results for "'+ search_term + '"'
        pods = db.search_pod_by_keyword(search_term)
    return render_template("search_results.html", \
        pods = pods, \
        offset = offset, \
        search_term = search_term, \
        table_title = table_title, \
        pod_placeholder = random.choice(pod_placeholders))

@app.route('/itunes_id=<itunes_id>&offset=<offset>', methods=['GET', 'POST'])
def show_results_id(itunes_id, offset = 0):
    offset = int(offset)
    pod = db.pod_lookup([itunes_id])
    recs = db.get_recommendations(itunes_id)
    plot_data = db.get_plotting_data()
    # plot_script, plot_div = make_cluster_plot(plot_data, pod, recs[offset:offset+10])
    plot_script, plot_div = make_cluster_plot(plot_data, pod, recs[offset:offset+10])

    return render_template("results.html", \
        plot_script = plot_script, plot_div = plot_div, \
        pod = pod, \
        pod_recommendations = recs, \
        offset = offset, \
        pod_placeholder = random.choice(pod_placeholders))

if __name__ == '__main__':
    app.run(port=33507)
