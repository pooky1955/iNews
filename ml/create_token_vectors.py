
from gensim.models import KeyedVectors
import pickle

def load_model(path_to_word2vec):
  """Loads google's word2vec 300 model"""
  model = KeyedVectors.load_word2vec_format(path_to_word2vec,binary=True)
  return model

def read_file(filepath):
  with open(filepath,"rt",encoding="utf-8") as f:
    return f.read()

print("Loading word2vec...")
word2vec_filepath = input("Enter filepath to word2vec model\n")

word2vec = load_model(word2vec_filepath)
print("Finished loading word2vec")
tokens = list(read_file("vocab.txt").split())
print(f"Finding corresponding vectors to {len(tokens)} tokens")

token_vectors = {}
for token in tokens:
  if token in word2vec:
    vector = word2vec[token]
    token_vectors[token] = vector

print("Tokens parsed to word2vec")
print(len(token_vectors.keys()))
with open("token_vectors.pickle","wb") as f:
  pickle.dump(token_vectors,f)



print("Finished creating tokens vector")