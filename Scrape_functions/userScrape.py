
#impport statements
import pandas as pd
import tweepy
import os

'''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''
def ScrapeTW(brand, path, lang='es', nUsers=20, nTweetsxUs=30, guardar=True):
    #API Keys
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    #Search Term
    search = str(brand)

    #Language to search (use standard 2-character ISO Code)
    language = lang

    #Output Path (Local or Server)
    outputPath = path

    #Number of users
    numUsers = nUsers

    #Number of tweets per user (MAX, may not always yield this amount)
    tweetsPerUser = nTweetsxUs

    '''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 
   

    #Authentication
    authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authentication.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authentication,  wait_on_rate_limit=True, wait_on_rate_limit_notify = True)

    #Query Constructor
    query = search + ' -filter:retweets -filter:replies'

    #Create columns for output csv
    tweets_dict = {"Profile Picture":[], "Username":[], "Name": [], "Location": [], "Query": [], "Text": [], "Date": [], "Followers": [], "CompiledText": []}
    countA = 1
    for tweet in tweepy.Cursor(api.search, q= query, lang = language, count = 100).items(numUsers):
        print("User: " + str(countA)) 
        tweets_dict["Name"].append(tweet.user.name)
        tweets_dict["Username"].append(tweet.user.screen_name)
        tweets_dict["Profile Picture"].append(tweet.user.profile_image_url_https)
        tweets_dict["Text"].append(tweet.text)
        tweets_dict["Query"].append(query)
        tweets_dict["Date"].append(tweet.created_at)
        tweets_dict["Followers"].append(tweet.user.followers_count)
        tweets_dict["Location"].append(tweet.user.location)
        completeText = ' '
        countB = 1
        for status in tweepy.Cursor(api.user_timeline, screen_name=tweet.user.screen_name , tweet_mode="extended").items(tweetsPerUser):
            print("User: " + str(countA) + " ~ Tweet " + str(countB))
            
            #FILTER REDUNANT RETWEETS
            toAdd = status.full_text
            if "RT" not in toAdd:
                completeText = completeText + toAdd
            countB += 1
            
        tweets_dict["CompiledText"].append(completeText)
        countA += 1
                
    #Make Dataframe
    tweets_data = pd.DataFrame(tweets_dict)
    
    #Print dataframe
    #print(tweets_data)
    
    #Output csv file
    if guardar:    
        filename = search + 'TwitterUsers' + '.csv'
        if(os.path.isdir(outputPath)==False):
            os.mkdir(outputPath)
        tweets_data.to_csv(os.path.join(outputPath, filename), index = False)
        
    return(tweets_data)
