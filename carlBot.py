import tweepy
import schedule
import time
import sys
import tweet_maker
 
argfile = str(sys.argv[1])

config_file = open('config.txt','r')
keys = config_file.read().splitlines()
config_file.close()
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = keys[0]
CONSUMER_SECRET = keys[1]
ACCESS_KEY = keys[2]
ACCESS_SECRET = keys[3]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def job():
    tweet_maker.make_tweet("exclamations.txt", "adverbs.txt", "adjectives.txt")
    
    filename=open(argfile,'r')
    tweets=filename.readlines()
    filename.close()
    
    for line in tweets:
        print(line)
        api.update_status(line)
        time.sleep(900)     #Tweet every 15 minutes

print("I have the current code")
schedule.every().day.at("18:00").do(job)
schedule.every().day.at("19:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute