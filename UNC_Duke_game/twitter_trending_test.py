import twitter
import json
import datetime
import time
import urlparse

#this part is to add KEY, SECRET and TOKEN for API access, generated from individual account, should be strings of letters
CONSUMER_KEY = "--------------------------------------"
CONSUMER_SECRET = "------------"
OAUTH_TOKEN = "------------------"
OAUTH_TOKEN_SECRET = "-------------------"

#twitter uses OAuth2.0 
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

#twitter_api is a twitter object generated by authorized API
twitter_api = twitter.Twitter(auth=auth)

#based on own knowledge, a collection of hashtags for each university was determined here. (It may not be accurate and complete)
#duke hashtags means this collection of hashtags are tend to be used by Duke supporters, while unc hashtags are used by UNC supporters
duke_hashtags = ["#GTHC", "#DukeNation", "#DUKEvsUNC ", "#BeatUNC", "#GoDuke", "#DukeGang", "#LetsGoDuke"]
unc_hashtags = ["#UNCvsDuke", "#uncnation", "#BeatDuke", "#BeatDook",  "#GDTBATH" , "#GoHeels", "#TarHeelNation",  "#UNCBBall"]

#generate queries
q1 = " OR ".join(duke_hashtags)
q2 = " OR ".join(unc_hashtags)

#twitter also has positive and negative setiment search for queries, which were planned to use but given up due to the limits for API requests
positive = " :)"
negative = " :("


def tweets_retrive(q, last_id, f):
    #q --> query, include_entitity --> get complete tweet information, max_id --> get tweets no newer than this id, count --> #. of tweets per page
    search_result = twitter_api.search.tweets(q = q, include_entities = 1, max_id= last_id, count = 100)
   #retrieve data
    statuses= search_result['statuses']
    
    #the returned data is more than one page, this step is to retrieve 50 pages ~100 tweets per page. 
    #Twitter has limit to over 10,000 tweets for each query,  and retrieve each page is an additional API request
    for _ in range(0, 50):
        try:
            #get next page
            next_results = search_result['search_metadata']['next_results']
        except KeyError, e:
            break
        next_results = urlparse.parse_qsl(next_results[1:])
        kwargs = dict(next_results)
        search_result = twitter_api.search.tweets(**kwargs)
        statuses += search_result['statuses']
    
    content = []
    #for analysis interests, only the content of tweets, locaiton of the user, hashtags, time of the tweet and the geo information is recorded into the file
    for status in statuses:
        tweet  = {}
        tweet['text'] = status['text']
        tweet['location'] = status['user']['location']
        hashtags = [i['text'] for i in status['entities']['hashtags']]
        tweet['hashtags'] = hashtags
        tweet['timestamp'] = status['created_at']
        tweet['geo'] = status['geo']
        #record the oldest id number during the retrieval
        if status['id']  < last_id:
            last_id= status['id']
        #only string can be written to the file. json.dump can be used to write dictionary files
        json.dump(tweet, f)
        f.write("\n")
    return last_id

#two independent information retrieval and analysis for each school
events = [ 'total_Duke', 'total_UNC']
qs = [q1, q2]

def main():
    #the order of retrieving information is from the recent to the start (max_id was used above), 
    #and the actual num of tweets are more than 50 pages.
    #So the oldest id num needs to be recorded to further retrieve the earlier tweets data
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
    
    #write tweets data to the file for future analysis
    last_tweets = [str(i) for i in last_tweets]
    l = open("last_ids.txt", 'w')
    l.write(",".join(last_tweets))
    l.close()
    
    #twitter limits the number of api request. 15 min for 180 requests, so each time the script waits 15mins for next run
    time.sleep(900)

#start run, needs ctrl+c to stop the script
while True :
   main()
   #print datetime.datetime.now()



