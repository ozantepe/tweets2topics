'''
Created on 2017-12-29

@author: Ozan Tepe
'''

# Twitter API credentials
consumer_key = "your_consumer_key";
consumer_secret = "your_consumer_secret";
access_token = "your_access_token";
access_secret = "your_access_secret";

# Twitter usernames
usernames = {
    "1": "andy_murray",
    "2": "DrOz",
    "3": "elonmusk",
    "4": "RealHughJackman",
    "5": "realDonaldTrump"
}
username = usernames["5"]

# Paths for file I/O
import os
project_dir = os.getcwd()
tweets_path = os.path.join(project_dir, 'tweets')
files_path = os.path.join(project_dir, 'files')
userfile_path = os.path.join(files_path, username)
