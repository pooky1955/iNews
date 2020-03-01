from bs4 import BeautifulSoup
import json
import requests
from pprint import pprint


class Snoper():
  def __init__(self):
    pass
  def search(self,keywords):
    query = '%20'.join(keywords)
    url = "https://yfrdx308zd-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.21.1%3Binstantsearch.js%201.11.15%3BJS%20Helper%202.19.0&x-algolia-application-id=YFRDX308ZD&x-algolia-api-key=7da15c5275374261c3a4bdab2ce5d321"
    body = '{"requests":[{"indexName":"wp_live_searchable_posts","params":"query='+query+'&hitsPerPage=10&page=0&facetingAfterDistinct=true&facets=%5B%22taxonomies_hierarchical.category.lvl0%22%2C%22post_author.display_name%22%2C%22post_date%22%5D&tagFilters="}]}'
    resp = requests.post(url,data=body)
    to_json = resp.json()
    hits = to_json["results"][0]["hits"]
    return hits
  def get_first(self,hits):
    hits = list(filter(lambda hit: hit["post_type"] == "fact_check",hits))
    
    first = hits[0]
    pprint(first)
    undefined_str = "__undefined__"
    
    data = dict(
      title = first.setdefault("post_title",undefined_str),
      snippet = first.setdefault("post_excerpt",undefined_str),
      rating = first["taxonomies"]["fact_check_rating"],
      claim = first.setdefault("fact_check_claim",undefined_str),
      url = first.setdefault("permalink",undefined_str),
      hasData = True
    )
    return data
  def search_one(self,keywords):
    hits = self.search(keywords)
    if len(hits) == 0:
      return None
    data = self.get_first(hits)
    return data

snoper = Snoper()
hit = snoper.search_one(["trump","kkk","father"])