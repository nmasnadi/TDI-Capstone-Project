from flask import Flask, render_template, request
from itunesSearch import search_pod

app = Flask(__name__)
pods = dict()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key_word = request.form['pod_name']
        pod_name, pod_image_url = search_pod(key_word)
        pods[pod_name] = pod_image_url

        return render_template("index.html", pods = pods)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(port=33507)
