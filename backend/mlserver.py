import json
from datetime import datetime
from pprint import pprint

import pandas as pd
from flask import Flask, app, request
from flask_cors import CORS

from ml_util import Filterer, Predictor
from web_util import GoogleScraper, get_host, extract_keywords
from mbfc import request_facts
from nltk.corpus import stopwords

app = Flask(__name__)
stopwords_set = set(stopwords.words('english'))
CORS(app)

google_scraper = GoogleScraper()
predictor = Predictor()
filterer = Filterer()


@app.route("/detect",methods=["POST"])
def fact_search():
  full_texts = []
  
  data = request.get_json()
  pprint(data)
  headline = data["headline"]
  keywords = extract_keywords(headline)
  print(f"KEYWORDS : {keywords}")
  df = request_facts(keywords) 
  
  filtered_ind = filterer.filter(headline,df["bodies"])
  filtered_df = pd.DataFrame(columns=["headlines","bodies","publishers","urls"])

  for headline_i, body_i, url_i, is_relevant in zip(df["headlines"],df["bodies"],df["urls"],filtered_ind):
    full_texts.append(f"{headline_i} : {is_relevant}\n\n{body_i}\n")    
    if is_relevant == 1:
      publisher_i = get_host(url_i)
      data = {
        'headlines' : headline_i,
        'bodies' : body_i,
        'urls' : url_i,
        'publishers' : publisher_i
      }
      filtered_df = filtered_df.append(data,ignore_index=True)


  print(filtered_df.head())
  stances = predictor.predict_stances(headline,filtered_df["bodies"])
  return_obj = dict( 
    stances = stances.tolist(),
    headlines = list(filtered_df["headlines"]),
    urls = list(filtered_df["urls"]),
    publishers=list(filtered_df["publishers"]),
    hasData = True
  )
  if len(filtered_df) == 0:
    return_obj = dict(hasData=False)
  return json.dumps(return_obj)


@app.route("/google-detect",methods=["POST"])
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
