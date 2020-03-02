import json
from pprint import pprint

from flask import Flask, app, request
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from mbfc import request_bias, request_facts
from snope_util import Snoper
from web_util import GoogleScraper, get_host


stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
google_scraper = GoogleScraper()

app = Flask(__name__)
CORS(app)

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
  if "http" in media:
    media = get_host(media)
  return json.dumps(request_bias(media))


@app.route("/extract",methods=["POST"])
def extract_info():
  data = request.get_json()
  url = data["url"]
  print(f"Url received : {url}")  
  data = google_scraper.get_info(url)
  return json.dumps(data)

@app.route("/")
def hello():
  return "Hello there"

if __name__ == "__main__":
  app.run(threaded=True,debug=False,host="0.0.0.0",port=5000)
