#import statements
import pandas as pd
from TwitterAPI import TwitterAPI
import json
import os
from datetime import date




def request_json(busqueda, marca,from_date,to_date):    
    #API Keys (Andrea)
    if to_date > int(date.today().strftime("%Y%m%d")+'0000'):
        print('Fecha posterior a hoy')
        return
    
    consumer_key = '' #API key
    consumer_secret = '' #API secret key
    access_token_key = '-'
    access_token_secret = ''
    PRODUCT='fullarchive'
    LABEL='Pruebas'
    #Authentication
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    #Create columns for output csv
    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                            {'query':"%s lang:es -retweet" %busqueda,
                            'fromDate':from_date,
                            'toDate':to_date})
    
    #r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
    #                    {'query':"prueba lang:es -retweet",
    #                   'fromDate':201901010000,
    #                    'toDate':201903010000})
    r_json = r.json()

    file_name1 = marca + str(from_date)+ "to" +  str(to_date) + '.json'
    file_name = r"Data\%s\Json\%s" % (marca, file_name1)

    with open(file_name, 'w') as json_file:
        json.dump(r_json, json_file)
        
    return(r_json)
    
def procesar_json(doc_json):

    #with open("Data\ejemplo\Json\ejemplo201901010000to201903010000.json") as json_file:
    #    r_json = json.load(json_file)

    tweets_dict = {"Fuente":[],"Text":[],"Retweets":[], "Favorites":[], "Date": [], "User Followers": [], "Username": [], "Location": [], "Verified": [], "Profile Picture": []}

    count = 1
    for tweet in doc_json['results']:
        print('Tweet: ' + str(count))
        tweets_dict["Fuente"].append('Twitter')
        try:
            tweets_dict["Text"].append(tweet["extended_tweet"]["full_text"])
        except:
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
        count+=1
    #Make Dataframe
    tweets_data = pd.DataFrame(tweets_dict)
    return(tweets_data)

'''
def guarda_csv(pd_file, path, filename):
    #Output csv file
    path = r"Data\%s\Csv"
    file_name = filename.replace(" ", "_")
    if(os.path.isdir(path)==False):
        os.mkdir(path)
    pd_file.to_csv(os.path.join(path, file_name), index = False)
    return(True)
'''

def scrape_full_archive(busqueda,marca, from_date, to_date): #, filename, path):
    if to_date > int(date.today().strftime("%Y%m%d")+'0000'):
        print('Fecha posterior a hoy')
    return
    
    r_json = request_json(busqueda,marca, from_date, to_date)
    #guardar = False
    tweets_pd = pd.DataFrame()
    if 'results' in r_json.keys():
        if r_json['results']!=[]:
            tweets_pd = procesar_json(r_json)
        #guardar = guarda_csv(tweets_pd, path, filename)
    #if(guardar != True):
    #    print("No se guardo el archivo")
    return (tweets_pd)

def crea_directorios(brand):
    path = r"Data\%s\Json" % brand
    if(os.path.isdir(path)==False):
        os.makedirs(path)


def Scrape_Iterativo(busqueda, brand, from_date, to_date, date_batch): #, filename, path, folder_name):
    '''
    This function will return a pd.DataFame object from the Twitter Scrape
    from: date in format YYYYMMDDHHSS
    to: date in format YYYYMMDDHHSS
    date_batch: number of days in format YYYYMMDDHHSS consider 100 tweets per request
    '''
    
    if to_date > int(date.today().strftime("%Y%m%d")+'0000'):
        print('Fecha posterior a hoy')
        return
    crea_directorios(brand)
    Twitter = pd.DataFrame()
    a = from_date  # a,b time batch limits
    b = a + date_batch
    aux = a
    #a = b
    #b = aux + date_batch
    while a < to_date:
        if b > to_date:
            b = to_date
        print("a: ", a," b: ",b)
        Twitter_aux = scrape_full_archive(busqueda, brand, a, b)#, filename, path)
        Twitter = Twitter.append(Twitter_aux, ignore_index=True)
        a = b
        b = a + date_batch
    Twitter.to_csv(r"Data\%s\Data_Raw_Twitter.csv" % brand)

    return(Twitter)


'''
Scrape_Iterativo("ejemplo",201901010000,201906010000,2000000)

marca="Loly in the sky"
from_date= 201810010000 
to_date=201910210000 
filename="Loly_Twitter_full.csv"
path="Ejemplo/Loly" 

r_json = request_json(marca,from_date,to_date)
tweets_pd = procesar_json(r_json)
#guardar=guarda_csv(tweets_pd, path, filename)

'''