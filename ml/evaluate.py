from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.callbacks import ModelCheckpoint, TensorBoard
import pickle
from tensorflow.python.keras.layers import Dense, Input, Dropout, Flatten, concatenate
from tensorflow.python.keras.layers.convolutional import Conv1D
from tensorflow.python.keras.layers.pooling import  MaxPool1D
from tqdm import tqdm
import numpy as np
from tensorflow.python.keras.layers.recurrent import LSTM
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.utils import plot_model
import pickle
from helpers import load_batch, dump_batch
import numpy as np
from constants import NUM_DIMENSIONS_WORD2VEC, HEADLINES_INPUT_LEN, BODIES_INPUT_LEN
# from gensim.models import KeyedVectors
import os
from datetime import datetime 

def load_token_vectors(filepath):
  with open(filepath,"rb") as f:
    return pickle.load(f)

def join(*paths):
  return '/'.join(paths)

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

def process_data(folder_prefix):

  headlines, bodies, one_hot_stances = load_batch(["headlines","bodies","one_hot_stances"],folder_prefix=folder_prefix)
  print("Dataset loaded")
  #encoding dataset
  token_vectors = load_token_vectors("token_vectors.pickle")
  
  encoded_bodies =encode_docs(bodies,token_vectors,NUM_DIMENSIONS_WORD2VEC,BODIES_INPUT_LEN)
  encoded_headlines =encode_docs(headlines,token_vectors,NUM_DIMENSIONS_WORD2VEC,HEADLINES_INPUT_LEN)
  print("Finished encoding dataset")

  Y_train = np.asarray(one_hot_stances)[:,:3]

  return encoded_headlines,encoded_bodies,Y_train

def save_doc(filename,text):
  with open(filename,"w") as f:
    f.write(text)

def evaluate(model,X,Y,name):
  preds = model.predict(X)
  harsh_preds = np.argmax(preds,axis=-1)
  harsh_y = np.argmax(Y,axis=-1)

  report = classification_report(harsh_y,harsh_preds,target_names=["Agree","Disagree","Discusses"])
  conf_matrix = confusion_matrix(harsh_y,harsh_preds)
  
  evaluate_str = '\n\n'.join((name,report,str(conf_matrix)))
  print(evaluate_str)

  # save_doc(f"report-{name}",evaluate_str)

def main():


  #shutting down kmp warnings
  os.environ["KMP_WARNINGS"] = "off"

  #loading dataset
  model_path = input("Enter model filepath")
  model = load_model(model_path) 


  encoded_headlines_train,encoded_bodies_train,Y_train = process_data("clean_training_data")
  encoded_headlines_valid,encoded_bodies_valid,Y_valid = process_data("clean_testing_data")

  evaluate(model,[encoded_headlines_train,encoded_bodies_train],Y_train,name=f"train-{model_path}")  
  evaluate(model,[encoded_headlines_valid,encoded_bodies_valid],Y_valid,name=f"valid-{model_path}")  


if __name__ == "__main__":
  main()


