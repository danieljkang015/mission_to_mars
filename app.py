from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_surfing


app = Flask(__name__)

client = PyMongo.MongoClient()
db = client.marsa_app
collection = db.mars_facts

@app.route("/")
def home():
    mars_data = list(db.mars_facts.find())

    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars = scrape_mars.scrape()
    print("\n\n\n")
    db.mars_facts.insert_one(mars)
    return "I scrapped some data for you"

if __name__ == "__main__":
    app.run(debug=True)
