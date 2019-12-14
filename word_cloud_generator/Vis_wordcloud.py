#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:30:43 2019

@author: nora
"""


import pandas as pd 
from pandas import DataFrame
import re
from nltk.tokenize import word_tokenize
import csv
import preprocessor as p
#from nltk.corpus import stopwords

from wordcloud import WordCloud
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display

import numpy as np
from PIL import Image
import matplotlib


############################## Preprocessing #################################   

def noramlize(text):
    
    text = str(text)
    text = re.sub(r"[إأٱآا]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"_", " ", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)
    
    
    # remove all characters that are not arabic letters
    text = re.sub(r'[^\u0620-\u064A]+', " ", text)
    
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



def prepareDataSets(tweets):
    cleand_tweets = []
    
    for index, row in tweets.iterrows():
        
        tweet = row['tweet']
        '''
        tweet = noramlize(tweet)
        tweet = p.clean(tweet) #Remove hashtag word
        '''
        tweet = stopWordRmove(tweet)
        
 
        label = row['predicted_label']
        if label == 0:
             cleand_tweets.append([tweet, '0'])
        else:
             cleand_tweets.append([tweet, '1'])
   
        
        
    df_cleand_tweets = DataFrame(cleand_tweets, columns=['tweet', 'predicted_label'])
    
    return df_cleand_tweets


 
    
###############################################################################

    
if __name__ == "__main__":
    

    tweets = pd.read_csv('../server/data/timeline_3 Dec_NoAdv_clean_noStopword_label.csv')

    c_tweets = prepareDataSets(tweets)
    
    #Positive
    p_data = c_tweets[c_tweets['predicted_label'] == '1']
    p_data = p_data['tweet']
    
    p_texts = p_data
    p_texts = [''.join(sentence) for sentence in p_texts]
    p_texts = ''.join(p_texts)
    
    p_reshaped_texts = arabic_reshaper.reshape(p_texts)
    p_arabic_texts = get_display(p_reshaped_texts)
    
    up_mask = np.array(Image.open("up.png"))
    
    wordcloud = WordCloud(width=700, height=300, background_color="white", font_path='Shoroq-Font.ttf', mask=up_mask).generate(p_arabic_texts)
    wordcloud.to_file("up_wordcloud.png") 
    
  
    #Negative
    n_data = c_tweets[c_tweets['predicted_label'] == '0']
    n_data = n_data['tweet']
    
    n_texts = n_data
    n_texts = [''.join(sentence) for sentence in n_texts]
    n_texts = ''.join(n_texts)
    
    n_reshaped_texts = arabic_reshaper.reshape(n_texts)
    n_arabic_texts = get_display(n_reshaped_texts)
    
    down_mask = np.array(Image.open("down.png"))
    
    wordcloud = WordCloud(width=700, height=300, background_color="white", font_path='Shoroq-Font.ttf', mask=down_mask, colormap=matplotlib.cm.inferno).generate(n_arabic_texts)
    wordcloud.to_file("down_wordcloud.png") 
    
    '''
    #All
    texts = c_tweets['tweet']
    texts = [''.join(sentence) for sentence in texts]
    texts = ''.join(texts)

    
    reshaped_texts = arabic_reshaper.reshape(texts)
    arabic_texts = get_display(reshaped_texts)
    
    mask_array = np.array(Image.open("down.png"))
    
    wordcloud = WordCloud(width=700, height=300, background_color="white", font_path='Shoroq-Font.ttf', mask=mask_array).generate(arabic_texts)
    wordcloud.to_file("wordcloud.png") 
 
    wordcloud.to_image()
   
    '''
    
 