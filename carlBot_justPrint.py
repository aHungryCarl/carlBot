import tweepy
import schedule
import time
import sys
import tweet_maker
 
argfile = str(sys.argv[1])
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'ON7VYEdsnLfRmry7a5wCfX57A'
CONSUMER_SECRET = 'bNFFQX66KBfuHjsRmUqW9PkcADdBmpIOJDXfmkU0pQNtTBTtJ0'
ACCESS_KEY = '718694695279308800-xnkB0FMuTekHyptngve0xyjf9XClFoz'
ACCESS_SECRET = 'KLzAMDtSjQ9UqAvRRCojI7sqRQeCuVIktCyVUpdLflB20'
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
        time.sleep(10)     #Tweet every 15 minutes

while True:
    job()