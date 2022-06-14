from fnd import app
from flask import request, render_template
from fnd.fnd import prediction

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    news = request.form['kutipan_berita']
    predictions = prediction(news)
    return render_template("index.html", predictions = predictions, news = news)