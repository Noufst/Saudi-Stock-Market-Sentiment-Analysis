#!/usr/bin/env python
# coding: utf-8

# # Required libraries
# 

# In[1]:


from kafka import KafkaConsumer
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.linear_model import SGDClassifier
import pickle
from word2vec import Word2Vec


# # Kafka consumer
# - setting the location of Kafka Broker
# - specifying the groupid and consumertimeout
# - subsribing to a topic




consumer = KafkaConsumer('stock_market',bootstrap_servers='localhost:9092', consumer_timeout_ms=30000)    


# # Prediction 


# read dataset
dataset_path = "final_dataset.csv"
dataset = pd.read_csv(dataset_path)
text = dataset['text_final']

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(text)
X_Tfidf = Tfidf_vect.transform(text)

# load the model
with open('modelsvm.pkl', 'rb') as fid:
    load_model = pickle.load(fid)
    
    

#predicting the streaming kafka messages    
print("Starting ML predictions.")
for message in consumer:    
    value = message.value.decode("utf-8", "strict") #add
    value = value.split("*;*") #add 
    
    tweet = value[0] #add 
    datetime = value[1] #add 
    
    X_new_tfidf = Tfidf_vect.transform([tweet])
    predicted = load_model.predict(X_new_tfidf)
    
    print("Tweet=%s, Datetime=%s, Sentiment=%s" % (tweet, datetime ,predicted[0]))






