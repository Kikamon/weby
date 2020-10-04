from flask import Flask, render_template
from random import choice

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/kamen")
def kamen():
    ja = "kámen"
    vysledek = choice(["kámen", "nůžky", "papír"])
    if vysledek == "kámen":
        skore = "REMÍZA"
    if vysledek == "nůžky":
        skore = "PROHRA"
    if vysledek == "papír":
        skore = "VÝHRA"
    return render_template("index.html", vysledek=vysledek, ja=ja, skore=skore)


@app.route("/nuzky")
def nuzky():
    ja = "nůžky"
    vysledek = choice(["kámen", "nůžky", "papír"])
    if vysledek == "kámen":
        skore = "PROHRA"
    if vysledek == "nůžky":
        skore = "REMÍZA"
    if vysledek == "papír":
        skore = "VÝHRA"
    return render_template("index.html", vysledek=vysledek, ja=ja, skore=skore)


@app.route("/papir")
def papir():
    ja = "papír"
    vysledek = choice(["kámen", "nůžky", "papír"])
    if vysledek == "papír":
        skore = "REMÍZA"
    if vysledek == "nůžky":
        skore = "VÝHRA"
    if vysledek == "kámen":
        skore = "PROHRA"
    return render_template("index.html", vysledek=vysledek, ja=ja, skore=skore)


if __name__ == "__main__":
    app.run()
