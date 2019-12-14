#!/usr/bin/env python
# coding: utf-8

# # Required libraries

# In[1]:


import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
from kafka import KafkaConsumer, KafkaProducer, SimpleProducer, KafkaClient
import json
import twitter_credentials


# # Twitter setup

consumer_key = twitter_credentials.CONSUMER_KEY
consumer_secret = twitter_credentials.CONSUMER_SECRET
access_token = twitter_credentials.ACCESS_TOKEN
access_token_secret = twitter_credentials.ACCESS_TOKEN_SECRET


# # Kafka producer
# 
# - specify the topic name
# 


# Kafka settings
topic_name = 'stock_market'
#setting up Kafka producer
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)


# # Kafka Broker
# 
# 1- querying the Twitter API Object
# 
# 2- extracting relevant information from the response
# 
# 3- formatting and sending the data to proper topic on the Kafka Broker
# 
# 4- resulting tweets have following attributes:
#         - tweet
# 


from datetime import datetime, timedelta #add

class KafkaPusher(StreamListener):
    def on_data(self, data):
        
        all_data = json.loads(data)
        tweet = all_data["text"]
        time = all_data["created_at"] #add
        
        mytime = datetime.strptime(time, "%a %b %d %H:%M:%S +0000 %Y") #add
        mytime += timedelta(hours=3) #add
        date = mytime.strftime("%Y-%m-%d %H:%M:%S") #add
        
        search = ['رابط التوصيات','مجاني','مجانيه','واتس','واتس اب','مجانا'] 
        if (any(x in tweet for x in search)):
            return

                
        record = '' #add
        record += str(tweet) #add
        record += '*;*' #add
        record += str(date) #add
        
        print ("Record: ", record)
        
        producer.send_messages(topic_name, record.encode('utf-8')) #update
        return True
    def on_error(self, status):
        print (status)

        

WORDS_TO_TRACK =   ['تاسي','#تاسي','السوق السعودي','#السوق_السعودي','ارتفاع سهم','انخفاض سهم','اكتتاب ارامكو','طرح ارامكو','المؤشر السعودي','قمم قيعان','#سوق_الاسهم','#سوق_الأسهم','سوق الاسهم','تداول','لمؤشرات المالية','الشارت','الربع الرابع','الربع الثالث','سهم نسبه','المؤشر العام', 'تداول', '#تداول_ارامكو']  

if __name__ == '__main__':
    l = KafkaPusher()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    while True:
        try:
            stream.filter(languages=["ar"], track=WORDS_TO_TRACK)
        except:
            pass       






