# from gensim.models import KeyedVectors
import os
import pickle
from datetime import datetime

import numpy as np
from tensorflow.python.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.python.keras.layers import (Dense, Dropout, Flatten, Input,
                                            concatenate)
from tensorflow.python.keras.layers.convolutional import Conv1D
from tensorflow.python.keras.layers.pooling import MaxPool1D
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.utils import plot_model
from tqdm import tqdm

from constants import (BODIES_INPUT_LEN, HEADLINES_INPUT_LEN,
                       NUM_DIMENSIONS_WORD2VEC)
from helpers import dump_batch, load_batch


def load_token_vectors(filepath):
  with open(filepath,"rb") as f:
    return pickle.load(f)

def join(*paths):
  return '/'.join(paths)

def define_model(bodies_max_len,headlines_max_len,word2vec_dimensions):
  """Returns a model used to predict stances"""
  #bodies input
  #channel1
  bodies_input = Input(shape=(bodies_max_len,word2vec_dimensions))
  
  bodies_conv1 = Conv1D(32,4,activation="relu",padding="same")(bodies_input)
  bodies_drop1 = Dropout(0.5)(bodies_conv1)
  bodies_pool1 = MaxPool1D()(bodies_drop1)
  bodies_flatten1 = Flatten()(bodies_pool1)
  
  bodies_conv2 = Conv1D(32,6,activation="relu",padding="same")(bodies_input)
  bodies_drop2 = Dropout(0.5)(bodies_conv2)
  bodies_pool2 = MaxPool1D()(bodies_drop2)
  bodies_flatten2 = Flatten()(bodies_pool2)
  
  bodies_conv3 = Conv1D(32,8,activation="relu",padding="same")(bodies_input)
  bodies_drop3 = Dropout(0.5)(bodies_conv3)
  bodies_pool3 = MaxPool1D()(bodies_drop3)
  bodies_flatten3 = Flatten()(bodies_pool3)


  headlines_input = Input(shape=(headlines_max_len,word2vec_dimensions))
  
  headlines_conv1 = Conv1D(32,4,activation="relu",padding="same")(headlines_input)
  headlines_drop1 = Dropout(0.5)(headlines_conv1)
  headlines_pool1 = MaxPool1D()(headlines_drop1)
  headlines_flatten1 = Flatten()(headlines_pool1)

  headlines_conv2 = Conv1D(32,6,activation="relu",padding="same")(headlines_input)
  headlines_drop2 = Dropout(0.5)(headlines_conv2)
  headlines_pool2 = MaxPool1D()(headlines_drop2)
  headlines_flatten2 = Flatten()(headlines_pool2)
  
  headlines_conv3 = Conv1D(32,8,activation="relu",padding="same")(headlines_input)
  headlines_drop3 = Dropout(0.5)(headlines_conv3)
  headlines_pool3 = MaxPool1D()(headlines_drop3)
  headlines_flatten3 = Flatten()(headlines_pool3)

  concat = concatenate([headlines_flatten1,headlines_flatten2,headlines_flatten3,bodies_flatten1,bodies_flatten2,bodies_flatten3])

  dense = Dense(100,activation="relu")(concat)
  output = Dense(3,activation="softmax")(dense)

  model = Model(inputs=[headlines_input,bodies_input],outputs=output)
  model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])
  model.summary()

  return model

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
  print(f"Training on {len(headlines)} samples.")
  #encoding dataset
  token_vectors = load_token_vectors("token_vectors.pickle")
  
  encoded_bodies =encode_docs(bodies,token_vectors,NUM_DIMENSIONS_WORD2VEC,BODIES_INPUT_LEN)
  encoded_headlines =encode_docs(headlines,token_vectors,NUM_DIMENSIONS_WORD2VEC,HEADLINES_INPUT_LEN)
  print("Finished encoding dataset")

  Y_train = np.asarray(one_hot_stances)[:,:3]

  print("Creating model...")
  return encoded_headlines,encoded_bodies,Y_train

def main():


  folder_path = "googleword2vec-multichannel-conv1d"
  #shutting down kmp warnings
  os.environ["KMP_WARNINGS"] = "off"

  unique_identifier = input("Enter an identifier for this training instance\n")
  #loading dataset
  model = define_model(BODIES_INPUT_LEN,HEADLINES_INPUT_LEN,NUM_DIMENSIONS_WORD2VEC)

  if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print(f"Creating model folder path {folder_path}")

  encoded_headlines_train,encoded_bodies_train,Y_train = process_data("clean_training_data")
  encoded_headlines_valid,encoded_bodies_valid,Y_valid = process_data("clean_testing_data")


  plot_model(model,to_file=f"{folder_path}/model.png",show_shapes=True)
  checkpoint = ModelCheckpoint(folder_path+f"/{unique_identifier}-"+"{epoch:02d}-{val_acc:.3f}.hdf5",monitor="val_acc",mode="auto",save_weights_only=False,verbose=1)
  logdir = f"{folder_path}/logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
  if not os.path.exists(logdir):
    os.makedirs(logdir)
    print(f"Created directory {logdir}")
  tensorboard = TensorBoard(log_dir=logdir)

  callbacks = [checkpoint,tensorboard]

  history = model.fit([encoded_headlines_train,encoded_bodies_train],Y_train,validation_data=[[encoded_headlines_valid,encoded_bodies_valid],Y_valid],epochs=100,shuffle=True,verbose=1,callbacks=callbacks)
  print("Finished training")

if __name__ == "__main__":
  main()
  # model = define_model(BODIES_INPUT_LEN,HEADLINES_INPUT_LEN,NUM_DIMENSIONS_WORD2VEC)
  # plot_model(model,to_file="deep_model.png",show_shapes=True)
