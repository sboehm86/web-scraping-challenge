from flask import Flask, redirect, render_template, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo=PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index(): 

    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

#trigger scrape
@app.route("/scrape")
def scrape(): 

    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.mars_scrape_news()
    mars_data = scrape_mars.mars_scrape_image()
    mars_data = scrape_mars.mars_scrape_faq()
    mars_data = scrape_mars.mars_scrape_hemi()
    mars_info.update({}, mars_data, upsert=True)

    return "Scrape Complete!"

if __name__ == "__main__": 
    app.run()