from googlesearch import search_news
from newspaper import Article
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from nltk.corpus import stopwords
import re
from string import punctuation
stopwords_set = set(stopwords.words("english"))


def extract_keywords(headline):
  tokens = headline.split(" ")
  punc_patt = re.compile(rf'[{punctuation}]')
  tokens = [punc_patt.sub("",token) for token in tokens]
  tokens = [token for token in tokens if not token in stopwords_set]
  tokens = [token for token in tokens if token.isalpha()]
  return tokens

def get_set_event_loop():
  try : 
    return asyncio.get_event_loop()
  except RuntimeError as e:
    if e.args[0].startswith('There is no current event loop'):
      asyncio.set_event_loop(asyncio.new_event_loop())
      return asyncio.get_event_loop()
    raise e

def get_bodies(urls):
  bodies = []
  filtered_urls = []

  loop = get_set_event_loop()
  loop.run_until_complete(
    asyncio.gather(
      *[get_url(url,bodies,filtered_urls) for url in urls]
    )
  )
  return bodies, filtered_urls

def get_host(url):
  without_http = url.split("//")[1]
  splitted = without_http.split(".")
  if splitted[0] == "www":
    return splitted[1]
  else:
    return splitted[0]

def parse_article(html):
  soup = BeautifulSoup(html,features="html.parser")
  p_tags = soup.find_all('p')
  title_tag = soup.find("title")
  try:
    title = title_tag.get_text()
  except:
    title = "Title not found :("

  paragraphs = [p_tag.get_text() for p_tag in p_tags]
  body = ' '.join(paragraphs)
  return body, title

async def get_url(url,bodies,urls):
  try :
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status == 200:
          data = await resp.text()
          bodies.append(data)
          urls.append(url)
  except Exception as e:
    print(f"Exception occured with url {url}")
class GoogleScraper():
  def __init__(self):
    pass
  def get_info(self,url):
    searched_article = Article(url)
    searched_article.download()
    searched_article.parse()
    
    headline = searched_article.title
    translator = Translator()
    headline = translator.translate(headline).text
    keywords = [token for token in headline.split()]
    keywords = [token for token in keywords if not token in stopwords_set]

    data = {
      'headline' : headline,
      'articleKeywords' : keywords,
    }

    return data

  def search(self,query,limit):
    df = pd.DataFrame()

    urls = self._search(query,limit)
    
    
    print("Found all urls")

    bodies, filtered_urls = get_bodies(urls)
    hosts = [get_host(url) for url in filtered_urls]
    print(f"Retrieved {len(bodies)} bodies")
    clean_bodies, clean_titles = parse_articles(bodies)

    df["bodies"] = clean_bodies
    df["headlines"] = clean_titles
    df["publishers"] = hosts
    df["urls"] = filtered_urls

    return df
  def _search(self,query,limit):
    urls = [url for url in search_news(stop=limit,query=query)]
    return urls
 
def parse_articles(bodies):
  parsed = [parse_article(body) for body in bodies]
  bodies = []
  titles = []
  for parsed_i in parsed:
    bodies.append(parsed_i[0])
    titles.append(parsed_i[1])
  return bodies, titles

if __name__ == "__main__":
  google_scraper = GoogleScraper()
  df_results = google_scraper.search("trump impeachment",10)
  print(df_results.head(5))