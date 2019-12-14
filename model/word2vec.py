#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:17:20 2019

@author: nouf
"""

from logging import info
from gensim.models import KeyedVectors
import numpy as np
from nltk.tokenize import wordpunct_tokenize
from sklearn.impute import SimpleImputer

class Word2Vec:
    
    def __init__(self):
        
        # vectors file
        self.embeddings_file = "arabic_embeddings.bin"
    
        self.embeddings, self.dimension = self.load_vectors()
        

    def getVectors(self, text):
        
        # -- dataset preprocessing -- #
        tokens = self.tokenize_data(text, 'text')

        # -- vectorize data -- #
        vectors = self.average_feature_vectors(tokens, 'tokens')

        # vectorized features
        return self.remove_nan(vectors)
    
        
        
    def load_vectors(self):
            
            """load the pre-trained embedding model"""
            w2v_model = KeyedVectors.load_word2vec_format(self.embeddings_file, binary=True, unicode_errors='ignore')
    
            w2v_model.init_sims(replace=True)  # to save memory
            vocab, vector_dim = w2v_model.vectors.shape
            return w2v_model, vector_dim
    
        
    def tokenize(self, text):
        """
        :param text: a paragraph string
        :return: a list of words
        """
    
        try:
            txt = text
            words = wordpunct_tokenize(txt)
            length = len(words)
        except TypeError:
            words, length = ['NA'], 0
    
        return words, length
    
    def tokenize_data(self, examples_txt, type_='NaN'):
        tokens = []
        info('Tokenizing the {} dataset ..'.format(type_))
        total_tokens = []
        for txt in examples_txt:
            words, num = self.tokenize(txt)
            tokens.append(words)
            total_tokens.append(num)
        info(' ... total {} {} tokens.'.format(sum(total_tokens), type_))
        return tokens
    
    def feature(self, words):
        """average words' vectors"""
        feature_vec = np.zeros((self.dimension,), dtype="float32")
        retrieved_words = 0
        for token in words:
            try:
                feature_vec = np.add(feature_vec, self.embeddings[token])
                retrieved_words += 1
            except KeyError:
                pass  # if a word is not in the embeddings' vocabulary discard it
    
        np.seterr(divide='ignore', invalid='ignore')
        feature_vec = np.divide(feature_vec, retrieved_words)
    
        return feature_vec
    
    def average_feature_vectors(self, examples, type_='NaN'):
        """
        :param examples: a list of lists (each list contains words) e.g. [['hi','do'], ['you','see'], ... ]
        :param type_: (optional) type of examples text 
        :return: the average word vector of each list
        """
    
        feature_vectors = np.zeros((len(examples), self.dimension), dtype="float32")
        info("Vectorizing {} tokens ..".format(type_))
        for i, example in enumerate(examples):
            feature_vectors[i] = self.feature(example)
    
        info(" ... total {} {}".format(len(feature_vectors), type_))
    
        return feature_vectors
    
    def remove_nan(self, x):
        """remove NaN values from data vectors"""
        imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
        imp_mean = imp_mean.fit(x)
        x_clean = imp_mean.transform(x)
        return x_clean