'''
© HALSmartia 2019

Algorithm scrapes tweets from the past week
to determine social sentiment factor for
a particular search.

@author: Andrea Vargas

Dependencies: PANDAS, TWITTERAPI, OS

@param: Brand Search Query, Number Tweets, Output Path
-uses twitter premium features tu access full archive sandbox. must create an app and assign the Enviroment in developer.twitter.com

@output: CSV file to specified path
'''

#import statements
import pandas as pd
from TwitterAPI import TwitterAPI
import json
import os


'''
||||||MODULAR|||||
'''

def request_json(marca, from_date,to_date):   
    ''' 
    #API Keys (Andrea)
    consumer_key = 'EVKtj6NUbhThsoTE04Si6jmUH'
    consumer_secret = 'xEE5pQDzvu7jrdV2RuYt9FvHO85U3UpHyfDlknHhiEUtoT4XMk'
    access_token_key = '190425302-7GzzejNNZHXgA5I9at2VLgLstzBFzIFpsis55PSn'
    access_token_secret = 'KAjZsY61jUqZx4FZmyLlKJ1utMBtbgGCdbtuNObsxMTQV'
    PRODUCT='fullarchive'
    LABEL='pruebasAVG'
    '''
    #API Keys (HAL SMARTIA)
    consumer_key = 'KEDe79qdMeqGqYm3fzfn11pvE'
    consumer_secret = 'O9KSpA3e6PlHdmSZdTtPvLUSClyiMcMGeWAiMUy9KSIjTz5NXI'
    access_token_key = '1168593743689265152-SvCu7k3NadQR4i9KEEgRjFleVP9CsI'
    access_token_secret = 'w8j1SoESTQjalPJruZWGBMF51bfV5FzAi8kwplEtULknn'
    PRODUCT='fullarchive'
    LABEL='Pruebas'
    


    #Authentication
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    #Create columns for output csv

    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                            {'query':marca,
                            'fromDate':from_date,
                           'toDate':to_date})

    r_json = r.json()
    file_name1 = marca + str(from_date)+ "to" +  str(to_date) + '.json'
    file_name = r"Data\%s\Json\%s" % (marca, file_name1)

    with open(file_name, 'w') as json_file:
        json.dump(r_json, json_file)
        
    return(r_json)


def procesar_json(doc_json):

    #with open(doc_json) as json_file:
    #    r_json = json.load(json_file)
    #API Keys (Andrea)
    consumer_key = 'EVKtj6NUbhThsoTE04Si6jmUH'
    consumer_secret = 'xEE5pQDzvu7jrdV2RuYt9FvHO85U3UpHyfDlknHhiEUtoT4XMk'
    access_token_key = '190425302-7GzzejNNZHXgA5I9at2VLgLstzBFzIFpsis55PSn'
    access_token_secret = 'KAjZsY61jUqZx4FZmyLlKJ1utMBtbgGCdbtuNObsxMTQV'

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

def scrape_full_archive(marca, from_date, to_date): #, filename, path):
    r_json = request_json(marca, from_date, to_date)
    #guardar = False
    tweets_pd = pd.DataFrame()
    if 'results' in r_json.keys():
        tweets_pd = procesar_json(r_json)
        #guardar = guarda_csv(tweets_pd, path, filename)
    #if(guardar != True):
    #    print("No se guardo el archivo")
    return (tweets_pd)

def crea_directorios(brand):
    path = r"Data\%s\Json" % brand
    if(os.path.isdir(path)==False):
        os.makedirs(path)


def Scrape_Iterativo(brand, from_date, to_date, date_batch): #, filename, path, folder_name):
    '''
    This function will return a pd.DataFame object from the Twitter Scrape
    from: date in format YYYYMMDDHHSS
    to: date in format YYYYMMDDHHSS
    date_batch: number of days in format YYYYMMDDHHSS consider 100 tweets per request
    '''
    crea_directorios(brand)

    a = from_date  # a,b time batch limits
    b = a + date_batch
    Twitter = scrape_full_archive(brand, a, b)#, filename, path)
    aux = a
    a = b
    b = aux + date_batch
    
    while a < to_date:
        if b > to_date:
            b = to_date        
        Twitter_aux = scrape_full_archive(brand, a, b)#, filename, path)
        Twitter = Twitter.append(Twitter_aux)
        aux = a
        a = b
        b = aux + date_batch

    Twitter.to_csv(r"Data\%s\Data_Raw.csv" % brand)

    return(Twitter)

'''
Twitter = Scrape_Iterativo("ejemplo",201901010000,201903010000,2010000 )
Twitter = pd.read_csv("Data\ejemplo\Data_Raw.csv")


marca="Loly in the sky"
from_date= 201810010000 
to_date=201910210000 
filename="Loly_Twitter_full.csv"
path="Ejemplo/Loly" 

r_json = request_json(marca,from_date,to_date)
tweets_pd = procesar_json(r_json)
#guardar=guarda_csv(tweets_pd, path, filename)

'''