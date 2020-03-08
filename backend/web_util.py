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
from log_util import info
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

def get_bodies(df):
  bodies = []
  urls = df["url"]
  titles = df["title"]
  filtered_urls = []
  filtered_titles = []
  indices = []
  loop = get_set_event_loop()
  loop.run_until_complete(
    asyncio.gather(
      *[get_url(url,title,bodies,filtered_urls,filtered_titles,indices,i) for i,(url,title) in enumerate(zip(urls,titles))]
    )
  )
  return bodies, filtered_urls, filtered_titles, indices

def get_host(url):
  without_http = url.split("//")[1]
  center =  without_http.split("/")[0]
  return center.split(".")[-2]

def parse_article(html):
  soup = BeautifulSoup(html,features="html.parser")
  p_tags = soup.find_all('p')

  paragraphs = [p_tag.get_text() for p_tag in p_tags]
  body = ' '.join(paragraphs)
  return body

async def get_url(url,title,bodies,urls,titles,indices,i):
  try :
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status == 200:
          data = await resp.text()
          bodies.append(data)
          urls.append(url)
          titles.append(title)
          indices.append(i)
  except Exception as e:
    print(f"Exception occured with url {url}")
def get_info(url):
    searched_article = Article(url)
    searched_article.download()
    searched_article.parse()
    
    headline = searched_article.title
    translator = Translator()
    translation = translator.translate(headline)
    headline = translation.text
    detected_language = translation.src
    info(f"Detected Language : {detected_language}")
    keywords = [token for token in headline.split()]
    keywords = [token for token in keywords if not token in stopwords_set]

    data = {
      'headline' : headline,
      'articleKeywords' : keywords,
    }

    return data


 
def parse_articles(bodies):
  parsed = [parse_article(body) for body in bodies]
  return parsed

if __name__ == "__main__":
  print("Web Util file successfully runned")