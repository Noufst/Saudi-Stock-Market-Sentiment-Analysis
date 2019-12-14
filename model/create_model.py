# coding: utf-8

"""
This is a simple Arabic Sentiment Analysis using Word Embeddings and Cross Validation.
Reference: https://github.com/iamaziz/ar-embeddings
Modified By: Amal Alazba, Nora Alturaief, Nouf Alturaief, Zainab Alhathloul
Date: Nov. 2019
"""

from logging import info
# -- 3rd party -- #
import pandas as pd
from warnings import simplefilter
import pickle
# -- classifiers -- #
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from word2vec import Word2Vec

class ArSentiment(object):
    
    def __init__(self, dataset_file=None, cv_folds=10):
        
        
        """
        :param embeddings_file: path to the embeddings file.
        :param dataset_file: path to a labeled dataset file.
        :param cv_folds: int, number of folds for cross validation
        """
        
        self.dataset_file = dataset_file
        self.cv_folds = cv_folds
        
        # read dataset
        dataset = pd.read_csv(self.dataset_file)
        text = dataset['tweet']
        self.Y = dataset['label']
        
        # Option 1-- word2vec using embedding -- #
        w2v = Word2Vec()
        self.X = w2v.getVectors(text, )
        
        # -- Option 2 count vectorization -- #
        #self.X = self.features_extraction(text)
        
        # -- Option 3 TFIDF -- #
        #self.X = self.tfidfFeatureExtraction(text)
    
        
        info('Done loading and vectorizing data.')
        info("--- Sentiment CLASSIFIERS ---")
        info("fitting ... ")

        self.accuracies = {}
        
        # classifiers to use
        classifiers = [
            #RandomForestClassifier(n_estimators=100),
            #SGDClassifier(),
            LinearSVC(),
            #LinearDiscriminantAnalysis(),
            #LogisticRegression(),
            #GaussianNB(),
            #DecisionTreeClassifier()
        ]
        
        
        # RUN classifiers
        for c in classifiers:
            self.classify(c)
        
        
        info('results ...')
        for k, v in self.accuracies.items():
            string = '\tAcc. {:.2f}% F1. {:.2f}% P. {:.2f} R. {:.2f} : {}'
            print(string.format(v[0] * 100, v[1] * 100, v[2] * 100, v[3] * 100, k))

        info("DONE!")
    

    def classify(self, classifier=None):

        classifier_name = classifier.__class__.__name__

        info('fitting data ...')
        info('\n\ncreated \n\n{}'.format(classifier))

        scores = cross_validate(classifier, self.X, self.Y, cv=self.cv_folds, scoring=('accuracy', 'precision', 'recall', 'f1'))
        f1_score = scores['test_f1'].mean()
        acc = scores['test_accuracy'].mean()
        recall = scores['test_recall'].mean()
        precision = scores['test_precision'].mean()

        results = [acc, f1_score, precision, recall]
        self.accuracies[classifier_name] = results
        
        self.saveModel(classifier)

    def saveModel(self, classifier):
        
        classifier.fit(self.X, self.Y)
        with open('model.pkl', 'wb') as fid:
            pickle.dump(classifier, fid)
         
    def tfidfFeatureExtraction(self, text):
    
        # min_df: ignore word that appear in less than 5 documents (tweets)
        # max_df: ignore words that appear in more than 75% of the documents (all tweets)
        # ngram_range=(1,3): to generate 2 and 3 word phrases along with single words from the corpus (e.g. if we had the sentence "Python is cool" we'd end up with 6 phrases - 'Python', 'is', 'cool', 'Python is', 'Python is cool' and 'is cool'.
        vectorizer = TfidfVectorizer(min_df=5, max_df=0.75, ngram_range=(1,3))
        #vectorizer = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1,2), sublinear_tf=True)
        
        # To get this: (tweet_index, feature_index) count
        tfidf_data = vectorizer.fit_transform(text)
        
        pickle.dump(vectorizer.vocabulary_, open("vocab.pkl", 'wb'))
            
        return tfidf_data
    

    def features_extraction(self, text):
        
        # create the transform
        vectorizer = CountVectorizer()
        # tokenize and build vocab
        vectorizer.fit(text)
        # summarize
        #print(vectorizer.vocabulary_)
        # encode document
        vector = vectorizer.transform(text)
        # summarize encoded vector
        #print(vector.shape)
        #print(type(vector))
        #print(vector.toarray())
        return vector.toarray()

        
if __name__ == "__main__":
    
    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    
    # dataset file
    dataset_path = "labeled_cleaned_tweets.csv"

    # run
    ArSentiment(dataset_path)
    