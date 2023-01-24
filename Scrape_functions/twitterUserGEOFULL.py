#import statements
import pandas as pd
from TwitterAPI import TwitterAPI
import json
import os


'''
||||||MODULAR|||||
'''

def request_json(query, from_date,to_date, lugar):   
    ''' 
    
    '''
    #API Keys (jc)
    consumer_key = '__'
    consumer_secret = '_'
    access_token_key = '_'
    access_token_secret = '_'
    PRODUCT='fullarchive'
    LABEL='Pruebas'
    


    #Authentication
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    #Create columns for output csv


    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                        {'query':"%s lang:es -retweet place:%s" % (query, lugar),
                        'fromDate':from_date,
                        'toDate':to_date})





    r_json = r.json()
    file_name1 = "%s_%s.json" % (query, lugar)
    file_name = r"ENTRENAMIENTO\BASES\JSON_LOC\%s" % file_name1

    with open(file_name, 'w') as json_file:
        json.dump(r_json, json_file)
        
    return(r_json)


def procesar_json(doc_json):
    
    
    consumer_key = '_'
    consumer_secret = '_'
    access_token_key = '_'
    access_token_secret = '_'
    
    #Authentication
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    

    tweets_dict = {"Text":[],"Retweets":[], "Favorites":[], "Date": [], "User Followers": [], "Username": [], "Location": [], "Verified": [], "Profile Picture": [], "Compiled Text":[]}

    countA = 1
    for tweet in doc_json['results']:
        print('User: ' + str(countA))
        tweets_dict["Text"].append(tweet['text'])
        tweets_dict["Retweets"].append(tweet['retweet_count'])
        tweets_dict["Favorites"].append(tweet['favorite_count'])
        tweets_dict["Date"].append(tweet['created_at'])
        #tweets_dict["Sentiment"].append(indicoio.sentiment(tweet.text))
        tweets_dict["User Followers"].append(tweet['user']['followers_count'])
        tweets_dict["Username"].append(tweet['user']['screen_name'])
        tweets_dict["Location"].append(tweet['user']['location'])
        tweets_dict["Verified"].append(tweet['user']['verified'])
        tweets_dict["Profile Picture"].append(tweet['user']['profile_image_url_https'])
        completeText = ' '
        countB = 1

        usr_id= tweet['user']['id']
        r_Us = api.request('statuses/user_timeline',
                                    {'count':50,
                                    'user_id': usr_id})
        r_Us_json= r_Us.json()
        for tweet in r_Us_json:
            print("User: " + str(countA) + " ~ Tweet " + str(countB))
            toAdd = tweet['text']
            completeText = completeText + toAdd
            countB += 1
        tweets_dict["Compiled Text"].append(completeText)

        countA +=1
    #Make Dataframe
    tweets_data = pd.DataFrame(tweets_dict)
    return(tweets_data)


def scrape_geo_full(query, from_date, to_date, lugar):
    r_json = request_json(query, from_date, to_date, lugar)

    tweets_pd = pd.DataFrame()
    if 'results' in r_json.keys():
        tweets_pd = procesar_json(r_json)
        #tweets_pd.to_csv( r"ENTRENAMIENTO\BASES\CSV_LOC\%s_%s" %(query, lugar ))

    return (tweets_pd)


