from requests_html import HTMLSession
import pandas as pd
from pprint import pprint
from web_util import get_bodies, parse_articles
from difflib import SequenceMatcher
import re


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
  for url in urls:
    all_results.extend(keywords_search(url))

  parsed_results = [parse_hit(hit) for hit in all_results]
  parsed_results = filter(lambda x : x != None,parsed_results)
  df = make_df(parsed_results)
  new_df = search_urls(df["url"])
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


def request_bias(media):
  hits = media_search(media,lim=4)  
  parsed_hits = [parse_media(hit) for hit in hits]
  if len(parsed_hits) == 0:
    return dict(hasData=False)
  else : 

    similarities = [similar(parsed_hit["name"],media) for parsed_hit in parsed_hits]
    argmax_simil, max_ratio = argmax(similarities)
    print(f"TOP RATIO : {max_ratio}") 
    chosen_hit = parsed_hits[argmax_simil]
    if chosen_hit["name"] == "Sources Pending":
      return dict(hasData=False)  
    else :
      return chosen_hit

def media_search(media,lim):
  session = HTMLSession()
  url = f"https://mediabiasfactcheck.com/?s={media}"
  resp = session.get(url)
  all_results = resp.html.find("article.status-publish")
  return all_results

def search_urls(urls):
  new_df = pd.DataFrame()
  bodies, filtered_urls = get_bodies(urls)
  parsed_bodies, parsed_titles = parse_articles(bodies)
  
  new_df["bodies"] = parsed_bodies
  new_df["urls"] = urls
  new_df["headlines"] = parsed_titles

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
  media = "tatersgonnatate"
  df = request_bias(media)
  print(df)
  print("Test done.")