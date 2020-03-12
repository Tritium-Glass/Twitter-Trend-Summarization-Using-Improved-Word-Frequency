#bot controller

from twitapi import get_trends
from web_scraping import get_articles
from common_trend_detector import get_topics
from text_summarization_module import get_summarized_article

class trend:
	def __init__(self,trend, useable_trend):
		self.trend = trend
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

	def __repr__(self):
		return '\ntrend '+str(self.trend)+'\narticles '+str(len(self.articles))+'\ntopics '+''.join(self.topic)


def main():

	trends = []

	raw_trends = get_trends()

	for key,value in get_trends().items():
		print(key)
		temp = trend(value,key)
		articles = get_articles(key)
		delete = []
		for i in range(len(articles)):
			if articles[i]=='':
				delete.append(i)
		for i in delete:
			del articles[i]
		if len(articles)==0:
			del temp
			continue
		temp.set_articles(articles)

		sum_articles = []
		try:
			if len(articles)>0:
				for article in articles:
					sum_articles.append(get_summarized_article(article))
				temp.set_summarized_articles(sum_articles)
				topic = get_topics(temp.articles)
				temp.set_topic(topic)
		except Exception as e:
			del temp
			continue
		print(temp)
		trends.append(temp)

	print('\n\n\n\n\n\n\n')
	print(raw_trends)
	for item in trends:
		print(item)

if __name__ == '__main__':
	main()
