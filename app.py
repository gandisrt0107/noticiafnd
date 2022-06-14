# from crypt import methods
# import imp
# from pyexpat import features

from flask import Flask, request, jsonify, render_template

from fnd import prediction

import os
import app 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    news = request.form['kutipan_berita']
    predictions = prediction(news)
    return render_template("index.html", predictions = predictions, news = news)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)