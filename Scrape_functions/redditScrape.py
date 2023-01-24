
#import dependencies
import praw
import pandas as pd
import datetime as dt
#import indicoio
import os

def RedditScrape(brand, path, since_month='month',  subreddit1='all'):

    '''~~~ FILL INFORMATION BELOW THIS LINE ~~~'''

    #API login requirements
    #indicoio.config.api_key = 'INDICOIO API KEY'
    #(redditKey )
    reddit = praw.Reddit(client_id='_',  
                    client_secret='_', 
                    user_agent='_', 
                    username='_', 
                    password='_')

    #search query
    brand = brand
    #brand = 'Samsung Galaxy S10'

    #Output Path (Local or Server)
    outputPath = path
    #outputPath = 'PATH'

    #History to search (day, week, month, year)
    since = since_month

    #Specify a subreddit (Set to 'all' for an unfiltered search)
    #subreddit = reddit.subreddit('all')
    subreddit = reddit.subreddit(subreddit1)
    
    '''~~~ FILL INFORMATION ABOVE THIS LINE ~~~''' 
    

    
    #Create columns for output csv
    #topics_dict = { "Post":[], "Score":[], "Upvote Ratio":[], "Comment Number": [], "subreddit": [], "Date": [], "Sentiment": []}
    topics_dict = { "Text":[], "Score":[], "Upvote Ratio":[], "Comment Number": [], "subreddit": [], "Date": []}
    
    #Fill columns from posts
    for submission in subreddit.search(brand, sort = 'new', time_filter = since):
        topics_dict["Text"].append(submission.title)
        topics_dict["Score"].append(submission.score)
        topics_dict["Upvote Ratio"].append(submission.upvote_ratio)
        topics_dict["Comment Number"].append(submission.num_comments)
        topics_dict["subreddit"].append(submission.subreddit.display_name)
        topics_dict["Date"].append(submission.created)
    #  topics_dict["Sentiment"].append(indicoio.sentiment(submission.title))

    #Make Dataframe
    topics_data = pd.DataFrame(topics_dict)
        
    #Change Date    
    def get_date(created):
        return dt.datetime.fromtimestamp(created)

    #Reassign Timestamp
    _timestamp = topics_data["Date"].apply(get_date)
    topics_data = topics_data.assign(timestamp = _timestamp)

    #Print dataframe
    print(topics_data)

    #Output csv file
    filename = brand + 'redditScrape' + '.csv'
    topics_data.to_csv(os.path.join(outputPath, filename), index = False)

    return topics_data
