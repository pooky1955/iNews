from helpers import load_batch, dump_batch
from tqdm import tqdm
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from sklearn.model_selection import train_test_split
from string import punctuation

stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_doc(document,counter):
  return ' '.join(extract_clean_tokens(document,counter))

def extract_clean_tokens(document,counter):
  
  tokens = document.split()
  tokens = [token.lower() for token in tokens]
  letter_patt = re.compile(rf"[{punctuation}]")
  tokens = [letter_patt.sub('',token) for token in tokens]  
  tokens = [token for token in tokens if len(token) > 1]
  tokens = [lemmatizer.lemmatize(token) for token in tokens]
  tokens = [token for token in tokens if not token in stopwords_set]
  update_vocab(tokens,counter)
  return tokens
def save_vocab(filename,vocab_list):
  text = '\n'.join(sorted(vocab_list))
  with open(filename,"w",encoding="utf-8") as f:
    f.write(text)
def update_vocab(tokens,counter):
  counter.update(tokens)

def clean_tokens(documents,keep_vocab_set):
  cleaned = []
  for document in documents:
    tokens = document.split()
    tokens = [token for token in tokens if token in keep_vocab_set]
    cleaned.append(' '.join(tokens))
  return cleaned



if __name__ == "__main__":
    headlines, bodies, one_hot_stances = load_batch(["headlines","bodies","one_hot_stances"],folder_prefix="related_data")
    vocab = Counter()


    clean_headlines = [clean_doc(headline,vocab) for headline in tqdm(headlines)]
    clean_bodies = [clean_doc(body,vocab) for body in tqdm(bodies)]
    # print(keep_vocab)

    min_occurence = 3
    
    keep_vocab = [word for word,count in dict(vocab).items() if count >= min_occurence ]
    print(f"Keep vocab len : {len(keep_vocab)}")
    save_vocab("vocab.txt",keep_vocab)
    keep_vocab_set = set(keep_vocab)
  

    clean_headlines = clean_tokens(clean_headlines,keep_vocab_set)
    clean_bodies = clean_tokens(clean_bodies,keep_vocab_set)

    clean_headlines_train, clean_headlines_test, clean_bodies_train, clean_bodies_test, one_hot_stances_train, one_hot_stances_test = train_test_split(clean_headlines,clean_bodies,one_hot_stances,test_size=0.2,random_state=42)
    

    dump_batch(["headlines","bodies","one_hot_stances"],[clean_headlines_train,clean_bodies_train,one_hot_stances_train],folder_prefix="clean_training_data")
    dump_batch(["headlines","bodies","one_hot_stances"],[clean_headlines_test,clean_bodies_test,one_hot_stances_test],folder_prefix="clean_testing_data")
