from flask import Flask, render_template
import os
import pymongo

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY")

# Database
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client.flaskDB

# Routes
from auth import routes

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/dashboard/")
def dashboard():
	return render_template("dashboard.html")

if __name__ == '__main__':
	app.run(debug=True)