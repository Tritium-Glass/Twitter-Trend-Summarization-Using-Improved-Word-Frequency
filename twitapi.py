import twitter,json,re

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

#print (mum_trends)
# print (json.dumps(trends, indent=1))
for trend in trends[0]["trends"]:
    try:
    	t = trend["name"].strip("#")
    	print(re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', t).lower())
    except Exception as e:
        pass
