from tqdm import tqdm


import os
import numpy as np
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from string import punctuation

from tensorflow.python.keras.models import load_model
import tensorflow as tf

HEADLINES_INPUT_LEN = 20
BODIES_INPUT_LEN = 500
NUM_DIMENSIONS_WORD2VEC = 300
graph = tf.get_default_graph()

def load_vocab(filename):
  with open(filename,"r",encoding="utf-8") as f:
    return set(f.read().split())

def load_token_vectors(filepath):
  with open(filepath,"rb") as f:
    return pickle.load(f)

def join(*paths):
  return '/'.join(paths)



def clean_doc(document,lemmatizer,stopwords_set=None):
  if stopwords_set != None:
    return ' '.join(extract_clean_tokens(document,lemmatizer,stopwords_set))
  else:
    return ' '.join(extract_clean_tokens(document,lemmatizer))

def filter_stopwords(document_tokens,stopwords_set):
  tokens = [token for token in document_tokens if not token in stopwords_set]
  return tokens

def extract_clean_tokens(document,lemmatizer=None,stopwords_set=None):
  
  tokens = document.split()
  tokens = [token.lower() for token in tokens]
  letter_patt = re.compile(rf"[{punctuation}]")
  tokens = [letter_patt.sub('',token) for token in tokens]  
  tokens = [token for token in tokens if len(token) > 1]
  if lemmatizer:
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
  if stopwords_set:
    tokens = [token for token in tokens if not token in stopwords_set]
  return tokens

def clean_tokens(documents,keep_vocab_set):
  cleaned = []
  for document in documents:
    tokens = document.split()
    tokens = [token for token in tokens if token in keep_vocab_set]
    cleaned.append(' '.join(tokens))
  return cleaned

def encode_docs(documents,token_vectors,num_dimensions_word2vec,max_len):
  """Encodes a text document so that the model can use it as input"""
  vectors_sequences = np.zeros(shape=(len(documents),max_len,num_dimensions_word2vec),dtype="float16")
  for document_ind,document in tqdm(enumerate(documents)):
    tokens = document.split()
    for i in range(min(max_len,len(tokens))):
      token = tokens[i]
      if token in token_vectors:
        vectors_sequences[document_ind,i] = token_vectors[token]
  
  return vectors_sequences


def fill_headline(encoded_headline,bodies_len):
  vectors = np.zeros((bodies_len,HEADLINES_INPUT_LEN,NUM_DIMENSIONS_WORD2VEC))
  for i in range(bodies_len):
    vectors[i] = encoded_headline
  return vectors
  

def process_data(headline,bodies,token_vectors,keep_vocab_set,lemmatizer,stopwords_set):
  clean_headlines = [clean_doc(headline,lemmatizer)]
  clean_bodies = [clean_doc(body,lemmatizer) for body in tqdm(bodies)]

  clean_headlines = clean_tokens(clean_headlines,keep_vocab_set)  
  clean_bodies = clean_tokens(bodies,keep_vocab_set)  

  return clean_headlines,clean_bodies

def predict(model,X):
  # as per https://stackoverflow.com/questions/51127344/tensor-is-not-an-element-of-this-graph-deploying-keras-model
  with graph.as_default():
    preds = model.predict(X)
  return np.argmax(preds,axis=-1)

def get_similarity(headline_set,body_set):
  return len(headline_set.intersection(body_set))

class Filterer():
  def __init__(self):
    
    with open("model/log_reg.pickle","rb") as f:
      self.log_reg = pickle.load(f)
    self.stopwords_set = set(stopwords.words("english"))


  # def filter_paragraphs(self,paragraphs)

  def filter(self,headline,bodies):
    #related are 1
    print(headline)
    headline_tokens = extract_clean_tokens(headline,stopwords_set=self.stopwords_set)
    bodies_tokens = [extract_clean_tokens(body,stopwords_set=self.stopwords_set) for body in bodies]
    
    headline_tokens_set = set(headline_tokens)
    headline_bodies_set = [set(body_tokens) for body_tokens in bodies_tokens]

    no_stopwords_headline_tokens_set = set(filter_stopwords(headline_tokens,self.stopwords_set))
    no_stopwords_bodies_tokens_set = [set(filter_stopwords(body_tokens,self.stopwords_set)) for body_tokens in bodies_tokens]

    inputs = np.array([get_similarity(no_stopwords_headline_tokens_set,body_tokens_set) for body_tokens_set in no_stopwords_bodies_tokens_set]).reshape(-1,1)
    # proba_preds = self.log_reg.predict_proba(inputs)[:,1]
    # print(proba_preds)
    # print(self.threshold)
    # preds = np.greater(self.threshold,proba_preds)
    preds = self.log_reg.predict(inputs)
    for body,pred in zip(bodies,preds):
      pred_str = "RELATED" if pred == 1 else "UNRELATED"
      print(body[:200])
      print(pred_str)
      print("="*40)
    return preds





class Predictor():
  def __init__(self):
    self.keep_vocab_set = load_vocab("model/vocab.txt")
    self.model = load_model("model/run1_allwords_nostopwords-24-0.943.hdf5")  
    self.token_vectors = load_token_vectors("model/token_vectors.pickle")
    self.stopwords_set = set(stopwords.words("english"))
    self.lemmatizer = WordNetLemmatizer()

  def predict_stances(self,headline,bodies):
    clean_headlines, clean_bodies = process_data(headline,bodies,self.token_vectors,self.keep_vocab_set,self.lemmatizer,self.stopwords_set)
    encoded_headlines = encode_docs(clean_headlines,self.token_vectors,NUM_DIMENSIONS_WORD2VEC,HEADLINES_INPUT_LEN)
    encoded_bodies = encode_docs(clean_bodies,self.token_vectors,NUM_DIMENSIONS_WORD2VEC,BODIES_INPUT_LEN)

    encoded_headlines = fill_headline(encoded_headlines[0],len(encoded_bodies))  
    stances = predict(self.model,[encoded_headlines,encoded_bodies])
    return stances
  

