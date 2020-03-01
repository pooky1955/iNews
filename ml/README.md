# iNews Machine Learning

Steps to run code on machine :

1. Git Clone Fake News Challenge dataset
2. Run `loader.py`, this will load the dataset into a folder called `related_data`
3. Run `preprocess.py`, it should create two new folders called `clean_training_data` and `clean_testing_data`
4. Run `create_token_vectors.py`, it will ask you the pathname to Google's Word2Vec and create `token_vectors.pickle`
5. Run `train_deep.py`. On my computer it achieved around ~ 97% accuracy on testing dataset

Feel free to clone and modify the code as you like!
