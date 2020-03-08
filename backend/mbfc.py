from requests_html import HTMLSession
import pandas as pd
from pprint import pprint
from web_util import get_bodies, parse_articles
from difflib import SequenceMatcher
import time
import re
from datetime import datetime
import numpy as np

def keywords_search(url):
  session = HTMLSession()
  resp = session.get(url)
  resp.html.render()
  all_results = resp.html.find("div.gs-webResult")
  return all_results



def parse_hit(hit):
  word_patt = re.compile(rf'[a-zA-Z]')
  if word_patt.match(hit.full_text) == None:
    return None
  title = hit.find(".gs-title",first=True).text
  url = hit.find("a.gs-title",first=True).attrs['href']
  description = hit.find("div.gs-snippet",first=True).text
  
  return {
   "title": title,
   "url" :  url,
   "description" : description
  }


def make_urls(keywords):
  query = '%20'.join(keywords)
  urls = []
  url = 'https://factualsearch.news/?fns.type=mostly-center&gsc.tab=0&gsc.q='+query+'&gsc.sort='
  for i in range(1,5):
    urls.append(f"{url}&gsc.page={i}")
  print(urls)
  return urls

def make_df(parsed_results):
  df = pd.DataFrame()
  for parsed_result in parsed_results:
    df = df.append(parsed_result,ignore_index=True)
  return df

def request_facts(keywords):
  urls = make_urls(keywords)
  all_results = []
  print("finished all urls")
  for url in urls:
    all_results.extend(keywords_search(url))
  print("finished appending keyword search")
  parsed_results = [parse_hit(hit) for hit in all_results]
  parsed_results = filter(lambda x : x != None,parsed_results)
  print("finished parsing hits")
  df = make_df(parsed_results)
  print("finished making dfs")
  new_df = search_urls(df)
  current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-results.csv")
  new_df.to_csv(current_date,encoding="utf-8",index=False)
  return new_df

def strip_spaces(text):
  return ''.join(text.split())

def similar(a,b):
  lower_a = a.lower()
  lower_b = b.lower()
  strip_a = strip_spaces(lower_a)
  strip_b = strip_spaces(lower_b)
  return SequenceMatcher(None,strip_a,strip_b).ratio()

def get_most_similar(name,hits):
  
  for hit in hits:
    hit_name = hit["name"]
  
def argmax(iterable_obj):
  max_ind = None
  max_el = 0
  for i,el in enumerate(iterable_obj):
    if el > max_el:
      max_el = el
      max_ind = i
  return max_ind, max_el


def extract_media_bias(description):
  category_names = []
  for token in description.split():
    if token == token.upper() and len(token) > 2:
      category_names.append(token)
    else:
      break
  return ' '.join(category_names)

def find_media_credibility(category_name):
  compressed = ''.join(category_name.lower().split())
  dubious_categories = ["questionablesource","conspiracy-pseudoscience"]
  return not compressed in dubious_categories

def request_bias(media):
  hits = media_search(media,lim=4)  
  parsed_hits = [parse_media(hit) for hit in hits]
  parsed_hits = [parsed_hit for parsed_hit in parsed_hits if parsed_hit["name"] != "Sources Pending"]
  if len(parsed_hits) == 0:
    return dict(hasData=False)
  else : 

    similarities = [similar(parsed_hit["name"],media) for parsed_hit in parsed_hits]

    argmax_simil, max_ratio = argmax(similarities)
    print(f"TOP RATIO : {max_ratio}") 
    chosen_hit = parsed_hits[argmax_simil]
    category = extract_media_bias(chosen_hit["description"])
    credibility = find_media_credibility(category)
    chosen_hit = dict(hasData=True,credibility=credibility,category=category,**chosen_hit)
    print(chosen_hit)
    return chosen_hit

def media_search(media,lim):
  session = HTMLSession()
  url = f"https://mediabiasfactcheck.com/?s={media}"
  resp = session.get(url)
  all_results = resp.html.find("article.status-publish")
  return all_results

def search_urls(urls):
  new_df = pd.DataFrame()
  bodies, filtered_urls, titles, indices = get_bodies(urls)
  parsed_bodies = parse_articles(bodies)
  
  new_df["bodies"] = parsed_bodies
  new_df["urls"] = filtered_urls
  new_df["headlines"] = titles

  return new_df
  



def parse_media(hit):
  a_tag = hit.find("a",first=True)
  url = a_tag.attrs["href"]
  media_name = a_tag.text
  description = hit.find(".mh-excerpt",first=True).text
  return {
    "description" : description,
    "url" : url,
    "name" : media_name
  } 

if __name__ == "__main__":
  print("Starting test.")
  keywords = ['trump','kkk','father']
  df = request_facts(keywords)
  print(df)
  
  print("Test done.")

  print("Starting test.")
  media = "breitbart"
  bias = request_bias(media)
  print(bias)
  print("Test done.")