import twitter
import json
import datetime
import time
import urlparse

CONSUMER_KEY = "--------------------------------------"
CONSUMER_SECRET = "------------"
OAUTH_TOKEN = "------------------"
OAUTH_TOKEN_SECRET = "-------------------"

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

duke_hashtags = ["#GTHC", "#DukeNation", "#DUKEvsUNC ", "#BeatUNC", "#GoDuke", "#DukeGang", "#LetsGoDuke"]
unc_hashtags = ["#UNCvsDuke", "#uncnation", "#BeatDuke", "#BeatDook",  "#GDTBATH" , "#GoHeels", "#TarHeelNation",  "#UNCBBall"]

q1 = " OR ".join(duke_hashtags)
q2 = " OR ".join(unc_hashtags)

positive = " :)"
negative = " :("


def tweets_retrive(q, last_id, f):
    search_result = twitter_api.search.tweets(q = q, include_entities = 1, max_id= last_id, count = 100)
    statuses= search_result['statuses']
    
    for _ in range(0, 50):
        print "Length of statuses", len(statuses)
        try:
            next_results = search_result['search_metadata']['next_results']
        except KeyError, e:
            break
        next_results = urlparse.parse_qsl(next_results[1:])
        kwargs = dict(next_results)
        search_result = twitter_api.search.tweets(**kwargs)
        statuses += search_result['statuses']
    
    content = []
    for status in statuses:
        tweet  = {}
        tweet['text'] = status['text']
        tweet['location'] = status['user']['location']
        hashtags = [i['text'] for i in status['entities']['hashtags']]
        tweet['hashtags'] = hashtags
        tweet['timestamp'] = status['created_at']
        tweet['geo'] = status['geo']
        if status['id']  < last_id:
            last_id= status['id']
        json.dump(tweet, f)
        f.write("\n")
    return last_id

#events= ['total_Duke', 'total_UNC', 'pos_Duke', 'neg_Duke', 'pos_UNC', 'neg_UNC']
events = [ 'total_Duke', 'total_UNC']
qs = [q1, q2]
#qs = [q1, q2, q1+positive, q1+negative, q2+positive, q2+negative]

def main():
    
    l = open("last_ids.txt", 'r')
    ids = l.readline()
    ids = ids.rstrip()
    ids = ids.split(',')
    last_tweets = [int(i) for i in ids]
    l.close()
    
   
    for i in range(len(events)):
        f = open(events[i]+'.txt', 'a')
        last_tweets[i] = tweets_retrive(qs[i], last_tweets[i], f)
        f.close()
    print last_tweets
    
    last_tweets = [str(i) for i in last_tweets]
    l = open("last_ids.txt", 'w')
    l.write(",".join(last_tweets))
    l.close()
    
    time.sleep(900)

while True :
   main()
   print datetime.datetime.now()



