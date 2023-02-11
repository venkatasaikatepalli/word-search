from flask import Flask

import sys, os
from flask import Flask
app = Flask(__name__)# URL Routing — Home Page

# Create a route to our index page at the root url, return a simple greeting
@app.route("/",methods=["GET"])
def indexPage():
	return open("index.html","r").read()

@app.route("/word/",methods=["POST"])
def wordSearch():
	return open("index.html","r").read()

# Main Function, Runs at http://0.0.0.0:8000
if __name__ == "__main__":
    app.run(port=8000)

