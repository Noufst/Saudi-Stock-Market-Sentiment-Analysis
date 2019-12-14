#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 11:55:31 2019

@author: nouf
"""

import pandas as pd
from pandas import DataFrame
import pickle
from word2vec import Word2Vec


if __name__ == "__main__":
    
    
    #dataset file
    dataset_path = "timeline_3Dec_NoAdv_cleaned.csv"

    # read dataset
    dataset = pd.read_csv(dataset_path)
    text = dataset['tweet'].values.astype('U')

    #result = svc.most_similar(positive=['بنت', 'فتاة'], negative=['ولد'], topn=1)
    #print(result)
    
    # convert words to vector using embeddings
    w2v = Word2Vec()
    x = w2v.getVectors(text)
    
    # load the model
    #svc = LinearSVC()
    with open('model.pkl', 'rb') as fid:
        svc = pickle.load(fid)
        
    # predict
    predicted_tweets = []
    y = svc.predict(x)
    for index, row in dataset.iterrows():
        print("Tweet=%s, Sentiment=%s" % (text[index], y[index]))
        predicted_tweets.append([row['id'], row['city'], row['country'], row['date'], row['hashtags'], text[index], y[index]])
     
    df_predicted_tweets = DataFrame(predicted_tweets, columns=['id', 'city', 'country', 'date', 'hashtags', 'tweet', 'sentiment'])
    df_predicted_tweets.to_csv (r'timeline_3Dec_NoAdv_cleaned_predicted.csv', index = None, header=True) 

    