"""OG VERSION OF SERVER"""
import json
from datetime import datetime
from pprint import pprint

import pandas as pd
from flask import Flask, app, request
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from mbfc import request_bias
from ml_util import Filterer, Predictor
from snope_util import Snoper
from web_util import GoogleScraper


stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


app = Flask(__name__)
CORS(app)

google_scraper = GoogleScraper()
predictor = Predictor()
filterer = Filterer()
snoper = Snoper()

def read_api_key(filename):
  with open(filename,"r") as f:
    return f.read()


def normalize(doc_tokens): 
  tokens = [token.lower() for token in doc_tokens]
  tokens = [lemmatizer.lemmatize(token) for token in tokens]
  tokens = [token for token in tokens if not token in stopwords_set]
  return tokens
  


@app.route("/snopecheck",methods=["POST"])
def snope_search():
  data = request.get_json()
  keywords = data["keywords"]
  keywords = [keyword.lower() for keyword in keywords if not keyword in stopwords_set]
  result = snoper.search_one(keywords)
  if result == None:
    return json.dumps(dict(hasData=False))
  print(result)
  title = result["title"]
  title_tokens = [token.lower() for token in title.split() if not token in stopwords_set]

  keywords_set = set(normalize(keywords))
  title_tokens_set = set(normalize(title_tokens))
  in_common = len(keywords_set.intersection(title_tokens_set))

  if in_common >= 2:
    return json.dumps(result)
  else:
    data = dict(hasData=False)
    return json.dumps(data)


@app.route("/mediacheck",methods=["POST"])
def media_search():
  data = request.get_json()
  pprint(data)
  media = data["name"]
  return json.dumps(request_bias(media))


@app.route("/factcheck",methods=["POST"])
def fact_search():
  current_str = datetime.now().strftime("%Y-%m-%D-%H-%M-%S")
  full_texts = []
  
  data = request.get_json()
  pprint(data)
  keywords = data["keywords"]
  headline = data["headline"]

  df = request_facts(keywords,lim=10) 
  
  filtered_ind = filterer.filter(headline,df["bodies"])
  filtered_df = pd.DataFrame(columns=["headlines","bodies","publishers","urls"])

  for headline_i, body_i, url_i, is_relevant in zip(df["headlines"],df["bodies"],df["urls"],filtered_ind):
    full_texts.append(f"{headline_i} : {is_relevant}\n\n{body_i}\n")    
    if is_relevant == 1:
      data = {
        'headlines' : headline_i,
        'bodies' : body_i,
        'urls' : url_i
      }
      filtered_df = filtered_df.append(data,ignore_index=True)


  with open(f"./results-{current_str}.txt","w") as f:
    f.write('\n'.join(full_texts))

  print(filtered_df)
  stances = predictor.predict_stances(headline,filtered_df["bodies"])
  return_obj = dict( 
    stance = stances.tolist()[0],
    headline = list(filtered_df["headlines"])[0],
    url = list(filtered_df["urls"])[0],
    hasData = True
  )
  if len(filtered_df) == 0:
    return_obj = dict(hasData=False)
  return json.dumps(return_obj)
  


@app.route("/extract",methods=["POST"])
def extract_info():
  data = request.get_json()
  url = data["url"]
  print(f"Url received : {url}")  
  data = google_scraper.get_info(url)
  return json.dumps(data)

@app.route("/detect",methods=["POST"])
def predict():
  data = request.get_json()
  headline = data["headline"]
  print(f"Headline received : {headline}")  
  df = google_scraper.search(headline,limit=30)

  filtered_ind = filterer.filter(headline,df["bodies"])
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
  app.run(threaded=True,debug=False,host="0.0.0.0")
