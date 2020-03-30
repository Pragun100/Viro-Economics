from flask import Flask
from flask import render_template, make_response
from flask import redirect, request, jsonify, url_for
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug = True)