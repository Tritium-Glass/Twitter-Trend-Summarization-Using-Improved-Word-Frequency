import tweepy,json,sys

consumer_key = 'S8gMgBFhScZ1PEQJqYmoDYcL9'
consumer_secret = 'SupHG06pkr15zhXyFA9W66fRejODbc7bKNnRILcrQoouG2cgbh'
access_token = '433140581-SbLJxTUuACh87NOJgOcZ3bexAeHELkbLN9Mzsu2K'
access_token_secret = '7r43Hsq38OxWpvbrVSQGzYoVUwLHnIRVSqRvIfcQVO7gD'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#api.update_status('Good Morning Everyone')

def get_tweets(username):
        # 200 tweets to be extracted -b
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username)

        tmp=[]

        tweets_for_csv = [tweet.text for tweet in tweets]
        for j in tweets_for_csv:
            tmp.append(j)
        print(tmp)

#get_tweets('gabrieldaking')

# Where On Earth ID for Brazil is 23424768.
WOEID = 2295411

trends = api.trends_place(WOEID)

trends = json.loads(json.dumps(trends, indent=1))

for trend in trends[0]["trends"]:
	print (trend["name"].strip("#"))
