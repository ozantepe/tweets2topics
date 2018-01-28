'''
Created on 2017-12-29

@author: Ozan Tepe
'''

import tweepy
import csv
import os
from datetime import datetime
from properties import consumer_key, consumer_secret, access_token, access_secret, username, tweets_path


def get_all_tweets(screen_name):
    
    # Twitter only allows access to a users most recent 3240 tweets with this method
    
    # Connect to Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    # Initialize tweepy
    api = tweepy.API(auth)
    
    # Initialize a list to hold all the tweets from tweepy
    all_tweets = []    
    
    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    
    # Save most recent tweets
    all_tweets.extend(new_tweets)
    
    # Save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    
    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("Getting tweets before %s" % (oldest))
        
        # All subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        
        # Save most recent tweets
        all_tweets.extend(new_tweets)
        
        # Update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1
        
        print("...%s tweets downloaded so far" % (len(all_tweets)))

    print("Tweets collected successfully..")
    
    # Transform tweets into a 2D array that will populate the csv    
    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]
    
    # Write tweets to the csv file
    date = str(datetime.now())[:19]
    date = date.replace(":", "-")
    filename = date + "_" + screen_name + "_tweets.csv"
    if not os.path.isdir(tweets_path):
        os.mkdir(tweets_path)
    fullpath = os.path.join(tweets_path, filename)  
    with open(fullpath, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(out_tweets)
    print("Saved to text file successfully..")


if __name__ == '__main__':
    get_all_tweets(username)
