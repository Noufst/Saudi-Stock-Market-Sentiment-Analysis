#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:18:11 2019

@author: nouf
"""

import pandas as pd 
from pandas import DataFrame
import re
from nltk.tokenize import word_tokenize
from nltk.stem.isri import ISRIStemmer
import csv
import itertools
import preprocessor as p
import warnings


def noramlize(text):
    
    text = str(text)
    text = re.sub(r"[إأٱآا]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"_", " ", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)
    
    # remove consecutive duplicate characters 
    #text = ''.join(ch for ch, _ in itertools.groupby(text))
    # remove all characters that are not arabic letters
    text = re.sub(r'[^\u0620-\u064A]+', " ", text)
    #text = re.sub(r'[^\u0620-\u064A\U0001F000-\U0001FFFF]+', " ", text)
    
    # remove al-harakat
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    
    # remove un-needed spaces 
    text = ' '.join(text.split())
    
    return text


def stopWordRmove(text):
    
    stop_words = []
    with open("my_stopwords.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for field in row:
                stop_words.append(field)
    
    words = word_tokenize(text)
    needed_words = []
    for word in words:
        if word not in stop_words:
            needed_words.append(word)
    filtered_sentence = " ".join(needed_words)
    return filtered_sentence



def stemming(text):
    st = ISRIStemmer()
    stemmed_words = []
    words = word_tokenize(text)
    for w in words:
        stemmed_words.append(st.stem(w))
    stemmed_sentence = " ".join(stemmed_words)
    return stemmed_sentence


def prepareDataSets(tweets):
    cleaned_tweets = []
    for index, row in tweets.iterrows():
        
        tweet = row['tweet']
        #tweet = noramlize(tweet)
        #tweet = p.clean(tweet)
        #tweet = stopWordRmove(tweet)
        tweet = stemming(tweet)
        
        cleaned_tweets.append([row['id'], tweet, row['label']])
     
    df_cleaned_tweets = DataFrame(cleaned_tweets, columns=['id', 'tweet', 'label'])
    df_cleaned_tweets.to_csv (r'labeled_cleaned_stemmed_tweets.csv', index = None, header=True) 
    
    return df_cleaned_tweets

    
if __name__ == "__main__":
    
    warnings.filterwarnings("ignore")
    
    # Read the csv file and construct the dataframe 
    df = pd.read_csv('labeled_cleaned_tweets.csv') 
    
    # Print the shape of the dataframe 
    #print(df.shape) 
    
    # Visualize the dataframe 
    #print(df.head(15)) 
    
    cleaned_tweets = prepareDataSets(df)
    #print(X);
    
    
    
    
    