import json
from datetime import datetime
from pprint import pprint

import pandas as pd
from flask import Flask, app, request
from flask_cors import CORS

from ml_util import Filterer, Predictor
from web_util import GoogleScraper

app = Flask(__name__)
CORS(app)

google_scraper = GoogleScraper()
predictor = Predictor()
filterer = Filterer()


@app.route("/detect",methods=["POST"])
def predict():
  data = request.get_json()
  headline = data["headline"]
  print(f"Headline received : {headline}")  
  df = google_scraper.search(headline,limit=30)

  filtered_ind = filterer.filter(headline,df["bodies"])
  print("Finished filtering")
  filtered_df = pd.DataFrame(columns=["headlines","bodies","publishers","urls"])
  
  for headline_i, body_i, publisher_i, url_i, is_relevant in zip(df["headlines"],df["bodies"],df["publishers"],df["urls"],filtered_ind):
    if is_relevant == 1:
      data = {
        'headlines' : headline_i,
        'bodies' : body_i,
        'publishers' : publisher_i,
        'urls' : url_i
      }
      filtered_df = filtered_df.append(data,ignore_index=True)
  print(filtered_df)
  stances = predictor.predict_stances(headline,filtered_df["bodies"])

  return_obj = dict( 
    stances = stances.tolist(),
    headlines = list(filtered_df["headlines"]),
    urls = list(filtered_df["urls"]),
    publishers = list(filtered_df["publishers"])
  )
  return json.dumps(return_obj)



@app.route("/")
def hello():
  return "Hello there"

if __name__ == "__main__":
  app.run(threaded=False,debug=False,host="0.0.0.0",port=5001)
