from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# # Or set inline
# client = PyMongo.MongoClient("mongodb://localhost:27017/")
# mars_info_dict=client.mars_app.mars_info_dict


@app.route("/")
def index():
    results = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=results)


@app.route("/scrape")
def scraper():  
    test_data = scrape_mars.scrape_all()
    # test_data={
    #     'test': 'test_data'
    # }
    mongo.db.mars.update({}, test_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
