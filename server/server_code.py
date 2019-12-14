#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 21:48:04 2019

@author: nouf
"""

from kafka import KafkaConsumer
import pickle
import pandas as pd
from flask import request
from flask import Flask
from flask_cors import CORS, cross_origin
import json
import csv 
from flask import Response
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model_file_name = "../model/modelsvm.pkl"

@app.route("/offline-sectors")
@cross_origin()
def sectors():
    
    Tweets = []
    sentiment = []
    
    with open("data/Data_13Dec_Clean_Labeled.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file, delimiter=',')
        for record in csv_reader:
            Tweets.append(record[5])
            sentiment.append(record[6])
        
         
    len(Tweets)
    
    counter3_neg=0
    counter3_pos=0
    counter4_neg=0 
    counter4_pos=0 
    counter5_neg=0
    counter5_pos=0
    counter6_neg=0
    counter6_pos=0
    counter7_neg=0
    counter7_pos=0
    counter8_neg=0
    counter8_pos=0
    counter9_neg=0
    counter9_pos=0

    for i, tweet in enumerate(Tweets):
                          
        if (("اسمنت" in tweet) or ("الاسمنت" in tweet) or ("الاسمنتات" in tweet)) and sentiment[i]=='0':
            counter4_neg=counter4_neg+1
        elif (("اسمنت" in tweet) or ("الاسمنت" in tweet) or ("الاسمنتات" in tweet)) and sentiment[i]=='1':
            counter4_pos=counter4_pos+1
            
        elif (("التامين" in tweet) or ("تكافل" in tweet) or ("للتكافل" in tweet)) and sentiment[i]=='0':
            counter5_neg=counter5_neg+1 
            
        elif (("التامين" in tweet) or ("تكافل" in tweet) or ("للتكافل" in tweet)) and sentiment[i]=='1':
            counter5_pos=counter5_pos+1 
            
        elif ("التجزيه" in tweet) and sentiment[i]=='0':
            counter7_neg=counter7_neg+1
            
        elif ("التجزيه" in tweet) and sentiment[i]=='1':
            counter7_pos=counter7_pos+1
            
        elif (("الزراعي" in tweet) or ("الزراعيه" in tweet)) and sentiment[i]=='0':
            counter8_neg=counter8_neg+1
            
        elif (("الزراعي" in tweet) or ("الزراعيه" in tweet)) and sentiment[i]=='1':
            counter8_pos=counter8_pos+1
            
        elif (("الاتصالات" in tweet) or ("اتصالات" in tweet)) and sentiment[i]=='0':
            counter6_neg=counter6_neg+1
            
        elif (("الاتصالات" in tweet) or ("اتصالات" in tweet)) and sentiment[i]=='1':
            counter6_pos=counter6_pos+1
            
        elif (("الريت" in tweet) or ("الريتات" in tweet) or ("ريت" in tweet) or ("العقار" in tweet) or ("العقاريه" in tweet)) and sentiment[i]=='0':
            counter9_neg=counter9_neg+1
            
        elif (("الريت" in tweet) or ("الريتات" in tweet) or ("ريت" in tweet) or ("العقار" in tweet) or ("العقاريه" in tweet)) and sentiment[i]=='1':
            counter9_pos=counter9_pos+1
            
        elif (("بنوك" in tweet) or ("البنوك" in tweet) or ("بنك" in tweet) or ("المصارف" in tweet)) and sentiment[i]=='0':
            counter3_neg=counter3_neg+1
            
        elif (("بنوك" in tweet) or ("البنوك" in tweet) or ("بنك" in tweet) or ("المصارف" in tweet)) and sentiment[i]=='1':
            counter3_pos=counter3_pos+1
         
    '''   
    print("البنوك انخفاض= ", counter3_neg)
    print("البنوك ارتفاع= ", counter3_pos)
    print("الاسمنت انخفاض= ", counter4_neg)
    print("الاسمنت ارتفاع= ", counter4_pos)
    print("التأمين انخفاض= ", counter5_neg)
    print("التأمين ارتفاع= ", counter5_pos)
    print("الاتصالات انخفاض= ", counter6_neg)
    print("الاتصالات ارتفاع= ", counter6_pos)
    print("التجزئه انخفاض= ", counter7_neg)
    print("التجزئه ارتفاع= ", counter7_pos)
    print("الزراعه انخفاض= ", counter8_neg)
    print("الزراعه ارتفاع= ", counter8_pos)
    print("العقار انخفاض= ", counter9_neg)
    print("العقار ارتفاع= ", counter9_pos)
    '''

    sectors = ('{"sectors" : [' +
                              '{"name": "البنوك", "pos": ' + str(counter3_pos) + ', "neg": ' + str(counter3_neg) + '},' +
                              '{"name": "الإسمنت", "pos": ' + str(counter4_pos) + ', "neg": ' + str(counter4_neg) + '},' +
                              '{"name": "التأمين", "pos": ' + str(counter5_pos) + ', "neg": ' + str(counter5_neg) + '},' +
                              '{"name": "الاتصالات", "pos": ' + str(counter6_pos) + ', "neg": ' + str(counter6_neg) + '},' +
                              '{"name": "التجزئة", "pos": ' + str(counter7_pos) + ', "neg": ' + str(counter7_neg) + '},' +
                              '{"name": "الزراعة", "pos": ' + str(counter8_pos) + ', "neg": ' + str(counter8_neg) + '},' +
                              '{"name": "العقار", "pos": ' + str(counter9_pos) + ', "neg": ' + str(counter9_neg) + '}' +
                              ']}')
    
    jData = json.loads(sectors)
    return jData


@app.route("/online-sectors")
@cross_origin()
def online_sectors():
    
    consumer = KafkaConsumer('stock_market',bootstrap_servers='localhost:9092', consumer_timeout_ms=30000)    

    # read dataset
    dataset_path = "data/tfidf_dataset.csv"
    dataset = pd.read_csv(dataset_path)
    text = dataset['text_final']
    
    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(text)
    
    # load the model
    with open(model_file_name, 'rb') as fid:
        load_model = pickle.load(fid)
    
    def events():
        
        for message in consumer:
            
            value = message.value.decode("utf-8", "strict") #add
            value = value.split("*;*") #add 
            
            tweet = value[0] #add  
            
            X_new_tfidf = Tfidf_vect.transform([tweet])
            y = load_model.predict(X_new_tfidf)
        
            sector = ""
            if (("اسمنت" in tweet) or ("الاسمنت" in tweet) or ("الاسمنتات" in tweet)):
                sector = "الإسمنت"
            elif (("التامين" in tweet) or ("تكافل" in tweet) or ("للتكافل" in tweet)):
                sector = "التأمين"  
            elif ("التجزيه" in tweet):
                sector = "التجزئة"
            elif (("الزراعي" in tweet) or ("الزراعيه" in tweet)):
                sector = "الزراعة"
            elif (("الاتصالات" in tweet) or ("اتصالات" in tweet)):
                sector = "الإتصالات"
            elif (("الريت" in tweet) or ("الريتات" in tweet) or ("ريت" in tweet) or ("العقار" in tweet) or ("العقاريه" in tweet)):
                sector = "العقار"
            elif (("بنوك" in tweet) or ("البنوك" in tweet) or ("بنك" in tweet) or ("المصارف" in tweet)):
                sector = "البنوك"
            
            print(tweet)
            
            if sector:
                json_string = '{"sentiment": "'+ str(y[0]) +'", "sector": "' + sector + '"}'
                print("###############")
                print(json.loads(json_string))
                yield "data: {}\n\n".format(json.dumps(json.loads(json_string)))
    
    return Response(events(), content_type='text/event-stream')


@app.route("/offline-aramco")
@cross_origin()
def sectors2():
    
    Tweets = []
    sentiment = []
    
    with open("data/Data_13Dec_Clean_Labeled.csv","r") as csv_file:
        csv_reader=csv.reader(csv_file, delimiter=',')
        for record in csv_reader:
            Tweets.append(record[5])
            sentiment.append(record[6])
        
         
    len(Tweets)
    
    counter1_neg=0
    counter1_pos=0
    counter2_neg=0
    counter2_pos=0
    counter10_neg=0
    counter10_pos=0

    for i, tweet in enumerate(Tweets):
            
        if (("ارامكو" in tweet) or ("أرامكو" in tweet)) and sentiment[i]=='0':
            counter1_neg=counter1_neg+1 
        
        elif (("ارامكو" in tweet) or ("أرامكو" in tweet)) and sentiment[i]=='1':
            counter1_pos=counter1_pos+1 
            
        elif (("الموشر العام" in tweet) or ("تاسي" in tweet)) and sentiment[i]=='0':
            counter2_neg=counter2_neg+1
            
        elif (("الموشر العام" in tweet) or ("تاسي" in tweet)) and sentiment[i]=='1':
            counter2_pos=counter2_pos+1
            
        elif sentiment[i]=='0':
            counter10_neg=counter10_neg+1
        
        else:
            counter10_pos=counter10_pos+1
          
    '''
    print("ارامكو انخفاض= ", counter1_neg)
    print("ارامكو ارتفاع= ", counter1_pos)
    print("المؤشر العام انخفاض=", counter2_neg)
    print("المؤشر العام ارتفاع=", counter2_pos)
    print("اخرى انخفاض= ", counter10_neg)
    print("اخرى ارتفاع= ", counter10_pos)
    '''

    sectors = ('{"sectors" : [' +
                              '{"name": "أرامكو", "pos": ' + str(counter1_pos) + ', "neg": ' + str(counter1_neg) + '},' +
                              '{"name": "المؤشر العام", "pos": ' + str(counter2_pos) + ', "neg": ' + str(counter2_neg) + '},' +
                              '{"name": "أخرى", "pos": ' + str(counter10_pos) + ', "neg": ' + str(counter10_neg) + '}' +
                              ']}')
    
    jData = json.loads(sectors)
    return jData


@app.route("/aramco-live")
@cross_origin()
def aramco_live():
    
    
    consumer = KafkaConsumer('stock_market',bootstrap_servers='localhost:9092', consumer_timeout_ms=30000)    

    # read dataset
    dataset_path = "data/tfidf_dataset.csv"
    dataset = pd.read_csv(dataset_path)
    text = dataset['text_final']
    
    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(text)
    
    # load the model
    with open(model_file_name, 'rb') as fid:
        load_model = pickle.load(fid)
    
    def events():
        
        for message in consumer:
            
            value = message.value.decode("utf-8", "strict") #add
            value = value.split("*;*") #add 
            
            tweet = value[0] #add  
            
            X_new_tfidf = Tfidf_vect.transform([tweet])
            y = load_model.predict(X_new_tfidf)
        
            sector = "أخرى"
            if (("ارامكو" in tweet) or ("أرامكو" in tweet)):
                sector = "أرامكو"
            elif (("الموشر العام" in tweet) or ("تاسي" in tweet)):
                sector = "المؤشر العام"
            
            tweet = tweet.replace('\n',' ')
            json_string = '{"sentiment": "'+ str(y[0]) +'", "sector": "' + sector + '"}'
            #print(json.loads(json_string))
            #print(tweet)
            yield "data: {}\n\n".format(json.dumps(json.loads(json_string)))
    
    
    return Response(events(), content_type='text/event-stream')

df = pd.read_csv("data/data2019.csv")
df=df.sort_values('date', ascending=True)
df['date'] = pd.to_datetime(df['date'])
df['dateDay'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['date'] = df['date'].dt.date
pos=[]
pos = df.groupby(['month','sentiment']).size() 
@app.route("/month")
@cross_origin()
def month():
    print('ooo')
    x = request.args.get('x')
    monthNo=0
    if(x=="Jan"):
        monthNo=1
    if(x=="Feb"):
        monthNo=2
    if(x=="Mar"):
        monthNo=3
    if(x=="Apr"):
        monthNo=4
    if(x=="May"):
        monthNo=5
    if(x=="Jun"):
        monthNo=6
    if(x=="Jul"):
        monthNo=7
    if(x=="Aug"):
        monthNo=8
    if(x=="Sep"):
        monthNo=9
    if(x=="Oct"):
        monthNo=10
    if(x=="Nov"):
        monthNo=11
    if(x=="Dec"):
        monthNo=12
    dt=df[df.month == monthNo]
    dt=dt.sort_values('dateDay', ascending=True)
    requiredDf=dt[['dateDay', 'sentiment']] 
    json = requiredDf.to_json(orient='records')
    print(json)
    return json

@app.route("/2d")
@cross_origin()
def twod():
    print('oo33')
    json = pos.to_json(orient='records')
    print(json)
    return json


@app.route("/liveChart2")
@cross_origin()
def liveChart2():  
    consumer = KafkaConsumer('stock_market',bootstrap_servers='localhost:9092', consumer_timeout_ms=20000)   
    dataset_path = "data/tfidf_dataset.csv"
    dataset = pd.read_csv(dataset_path)
    text = dataset['text_final']
    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(text)
        # load the model
    with open(model_file_name, 'rb') as fid:
        load_model = pickle.load(fid) 
        
    def events(): 
        for message in consumer:
            value = message.value.decode("utf-8", "strict") #add
            value = value.split("*;*") #add 
            tweet = value[0] #add 
            datetime1 = value[1] #add 
            date_time_obj = datetime.datetime.strptime(datetime1, '%Y-%m-%d %H:%M:%S')
            time=date_time_obj.time()
            time1=str(time)
            time1 = time1.split(":")
            print("tit"+time1[0])
            X_new_tfidf = Tfidf_vect.transform([tweet])
            predicted = load_model.predict(X_new_tfidf)  
            #json_string = '{"sentiment": "'+ str(predicted[0]) +'", "date": "' + str(time)+":"+time1[1] + '"}'
            json_string = '{"sentiment": "'+ str(predicted[0]) +'", "date": "' + str(time) + '"}'
            print(json.loads(json_string))
            yield "data: {}\n\n".format(json.dumps(json.loads(json_string)))
                
    return Response(events(), content_type='text/event-stream')

dfA = pd.read_csv("data/aramco2019.csv")
df1A = pd.read_csv("data/aramco2019.csv")
dfA=dfA[dfA.sector=="aramco"]
df1A=df1A[df1A.sector=="aramco"]
df1A=df1A.sort_values('date', ascending=True)
df1A['date'] = pd.to_datetime(df1A['date'])
df1A['date'] = df1A['date'].dt.date
d1A=dfA[dfA.sentiment == 1]
d2A=dfA[dfA.sentiment == 0]
d3=dfA
dfA['date'] = pd.to_datetime(dfA['date'])
dfA['dateDay'] = dfA['date'].dt.day
dfA['month'] = dfA['date'].dt.month
posA=[]
posA = dfA.groupby(['month','sentiment']).size() 
@app.route("/aramcoMonth")
@cross_origin()
def aramcoMonth():
    x = request.args.get('x')
    monthNo=0
    if(x=="Jan"):
        monthNo=1
    if(x=="Feb"):
        monthNo=2
    if(x=="Mar"):
        monthNo=3
    if(x=="Apr"):
        monthNo=4
    if(x=="May"):
        monthNo=5
    if(x=="Jun"):
        monthNo=6
    if(x=="Jul"):
        monthNo=7
    if(x=="Aug"):
        monthNo=8
    if(x=="Sep"):
        monthNo=9
    if(x=="Oct"):
        monthNo=10
    if(x=="Nov"):
        monthNo=11
    if(x=="Dec"):
        monthNo=12
    dt=dfA[dfA.month == monthNo]
    dt=dt.sort_values('dateDay', ascending=True)
    requiredDf=dt[['dateDay', 'sentiment']] 
    json = requiredDf.to_json(orient='records')
    return json
@app.route("/aramco")
@cross_origin()
def aramco():
    json = posA.to_json(orient='records')
    return json
 
if __name__ == "__main__":
    app.run()
    
if __name__ == "__main__":
    app.run()
    

    
    