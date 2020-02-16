import twitter,json,re,nltk
#nltk.download('words')
from langdetect import detect

consumer_key = 'S8gMgBFhScZ1PEQJqYmoDYcL9'
consumer_secret = 'SupHG06pkr15zhXyFA9W66fRejODbc7bKNnRILcrQoouG2cgbh'
access_token = '433140581-SbLJxTUuACh87NOJgOcZ3bexAeHELkbLN9Mzsu2K'
access_token_secret = '7r43Hsq38OxWpvbrVSQGzYoVUwLHnIRVSqRvIfcQVO7gD'

auth = twitter.oauth.OAuth(access_token, access_token_secret,
                           consumer_key, consumer_secret)

twitter_api = twitter.Twitter(auth=auth)


WORLD_WOE_ID = 1
US_WOE_ID = 23424977
Mumbai = 2295411


# world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
# us_trends = twitter_api.trends.place(_id=US_WOE_ID)
trends = twitter_api.trends.place(_id=Mumbai)
#words = set(nltk.corpus.words.words())
exact = []
pro = []
rank = []
c=0
#print (mum_trends)
# print (json.dumps(trends, indent=1))

for trend in trends[0]["trends"]:
	r = trend["tweet_volume"]
	rank.append(r)
rank
print(rank)

for trend in trends[0]["trends"]:
    try:
    	if(c<=10):
	    	e = trend["name"]
	    	t = e.strip("#")
	    	tt = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', t).lower()
	    	l = len(tt)
	    	b = tt[l-1]
	    	a = tt[0]
	    	if(ord(a)<=122 and ord(a)>=97):
	    		if(ord(b)<=122 and ord(b)>=97):
	    			 pro.append(tt)
	    			 exact.append(e)	
	    			 c = c+1
    except Exception as e:
        pass

tds = dict( zip(pro,exact))
#print(tds)
#print(trends[0]["trends"]) 



# Do not try,this shit works on my twitter handle dont tweet pls
############def post_tweet(summary):
	# Update your status

	#twitter_api.statuses.update(status=summary)

#####################post_tweet("Good Morning")