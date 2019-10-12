from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    scraped_data = mongo.db.scraped_data.find_one()
    return render_template("index.html", scraped_data=scraped_data)


@app.route("/scrape")
def scraper():
    scraped_data = mongo.db.scraped_data
    scraped_data_data = scrape_mars.scrape()
    scraped_data.update({}, scraped_data_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
