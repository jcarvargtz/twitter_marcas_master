#impport statements
import pandas as pd
import tweepy
#import indicoio
import nltk
import os




'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''
def TwitterScrape ( marca , path , n=20, lang='es'):  #marca: parametro a buscar, n=cantidad de tweets

    #class constants (apply filters as necessary)
    #brand = 'S10 -filter:retweets'
    brand = str(marca) + ' -filter:retweets'

    #Number of tweets to fetch (recommended limit to prevent timeout - 1000)
    numTweets = n

    #Local output path
    #outputPath = 'PATH'
    outputPath=path

    #Language to search (use standard 2-character ISO Code)
    #language = 'es'
    language = lang

    #API Keys (Andrea)
    consumer_key = 'EVKtj6NUbhThsoTE04Si6jmUH'
    consumer_secret = 'xEE5pQDzvu7jrdV2RuYt9FvHO85U3UpHyfDlknHhiEUtoT4XMk'
    access_token = '190425302-7GzzejNNZHXgA5I9at2VLgLstzBFzIFpsis55PSn'
    access_token_secret = 'KAjZsY61jUqZx4FZmyLlKJ1utMBtbgGCdbtuNObsxMTQV'
    #indicoio.config.api_key = 'INDICOIO API KEY'

    '''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 
    
    

    #Authentication
    authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authentication.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authentication, wait_on_rate_limit=True)

    #Create columns for output csv
    #tweets_dict = {"Text":[],"Retweets":[], "Favorites":[], "Date": [], "Sentiment": [], "User Followers": [], "Username": [], "Location": [], "Verified": [], "Profile Picture": []}
    tweets_dict = {"Text":[],"Retweets":[], "Favorites":[], "Date": [], "User Followers": [], "Username": [], "Location": [], "Verified": [], "Profile Picture": []}

    count = 1
    for tweet in tweepy.Cursor(api.search, q=brand, lang = language).items(numTweets):
        #print('Tweet: ' + str(count))
        tweets_dict["Text"].append(tweet.text)
        tweets_dict["Retweets"].append(tweet.retweet_count)
        tweets_dict["Favorites"].append(tweet.favorite_count)
        tweets_dict["Date"].append(tweet.created_at)
        #tweets_dict["Sentiment"].append(indicoio.sentiment(tweet.text))
        tweets_dict["User Followers"].append(tweet.user.followers_count)
        tweets_dict["Username"].append(tweet.user.screen_name)
        tweets_dict["Location"].append(tweet.user.location)
        tweets_dict["Verified"].append(tweet.user.verified)
        tweets_dict["Profile Picture"].append(tweet.user.profile_image_url_https)
        count+=1

    #Make Dataframe
    tweets_data = pd.DataFrame(tweets_dict)

    #Print dataframe
    print(tweets_data)

    #Output csv file
    filename = marca + "Twitter" + ".csv"
    if(os.path.isdir(outputPath)==False):
        os.mkdir(outputPath)
    tweets_data.to_csv(os.path.join(outputPath, filename), index = False)
        


'''
Para probar el código de la función Twitter Scrape corra las siguientes líneas

pathEjemplo=os.path.join(os.getcwd(),"Ejemplo") 
TwitterScrape("Samsung", pathEjemplo)

'''

