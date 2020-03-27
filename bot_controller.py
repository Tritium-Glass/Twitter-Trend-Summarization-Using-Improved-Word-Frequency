#bot controller

from twitapi import get_trends,post_tweet
from web_scraping import get_articles
from common_trend_detector import get_topics, compare_trends
from text_summarization_module import get_summarized_article
import traceback
import contextlib

try:
    from urllib.parse import urlencode

except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen

except ImportError:
    from urllib2 import urlopen

import sys

class trend:
	def __init__(self,exact_trend, useable_trend):
		self.exact_trend = exact_trend
		self.useable_trend = useable_trend
		self.articles = []
		self.summarized_articles = []
		self.topic = []

	def set_articles(self,articles):
		self.articles = articles

	def set_summarized_articles(self,articles):
		self.summarized_articles = articles

	def set_topic(self,topic):
		self.topic = topic

	def get_tweet(self):
		if self.exact_trend[0]=='#':
			return self.summarized_articles[0]+' '+make_tiny(self.articles[0].link)+' '+self.exact_trend
		else:
			return self.summarized_articles[0]+' '+make_tiny(self.articles[0].link)+' #'+'_'.join(self.exact_trend.split(' '))

	def __repr__(self):
		return '\ntrend '+str(self.useable_trend)+'\narticles '+str(len(self.articles))+'\ntopics '+str(self.topic)

def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')

def main():

	trends = []

	raw_trends = get_trends()

	for key,value in get_trends().items():
		#print(key)
		temp = trend(value,key)
		articles = get_articles(key)
		delete = []
		for i in range(len(articles)):
			if articles[i].text=='':
				delete.append(i)
		for i in delete:
			del articles[i]
		if len(articles)==0:
			del temp
			continue
		for i in range(len(articles)-1):
			for j in range(i+1,len(articles)):
				if articles[i].article_age < articles[j].article_age:
					articles[i],articles[j] = articles[j],articles[i]

		temp.set_articles(articles)

		sum_articles = []
		try:
			temp_articles = []
			for article in articles:
				sum_articles.append(get_summarized_article(article.text))
				temp_articles.append(article.text)
			temp.set_summarized_articles(sum_articles)

			# topic = get_topics(temp_articles)
			# temp.set_topic(topic)
		except Exception as e:
			print(traceback.format_exc())
			del temp
			continue
		#print(temp)
		trends.append(temp)

	# for i in range(len(trends)-1):
	# 	for j in range(i+1,len(trends)):
	# 		if compare_trends(trends[i].topic,trends[j].topic):
	# 			#print('similar trends')
	# 			del trend[j]

	print('\n\n\n')
	print(raw_trends)
	for item in trends:
		print(item.get_tweet())
		post_tweet(item.get_tweet())

if __name__ == '__main__':
	main()
