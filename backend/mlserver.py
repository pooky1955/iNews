import json
from datetime import datetime
from pprint import pprint

import pandas as pd
from flask import Flask, app, request
from flask_cors import CORS

from ml_util import Filterer, Predictor
from web_util import  get_host, extract_keywords
from mbfc import request_facts
from nltk.corpus import stopwords
from log_util import alert, finish, info

app = Flask(__name__)
stopwords_set = set(stopwords.words('english'))
CORS(app)

predictor = Predictor()
filterer = Filterer()


@app.route("/detect",methods=["POST"])
def fact_search():
  full_texts = []
  
  data = request.get_json()
  pprint(data)
  headline = data["headline"]
  keywords = extract_keywords(headline)
  alert(f"received new data {headline}")
  print(f"KEYWORDS : {keywords}")
  df = request_facts(keywords) 
  info("Finished making facts df")
  
  filtered_ind = filterer.filter(headline,df["bodies"])
  filtered_df = pd.DataFrame(columns=["headlines","bodies","publishers","urls"])
  info("Finished Filtering texts")
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
  finish("Responded to detect endpoint")
  return json.dumps(return_obj)



@app.route("/")
def hello():
  return "Hello there"

if __name__ == "__main__":
  alert("app is running")
  print("was there an alert printed above???")
  app.run(threaded=False,debug=False,host="0.0.0.0",port=5001)
