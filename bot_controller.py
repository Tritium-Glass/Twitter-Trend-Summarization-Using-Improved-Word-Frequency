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
		return 'trend '+str(self.trend)+'articles'+str(len(self.articles))+'topics'+''.join(self.topic)


def main():

	trends = []

	for key,value in get_trends().items():
		print(key)
		temp = trend(value,key)
		articles = get_articles(key)
		temp.set_articles(articles)
		sum_articles = []
		if len(articles)>0:
			for article in articles:
				sum_articles.append(get_summarized_article(article))
			temp.set_summarized_articles(sum_articles)
			topic = get_topics(temp.articles)
			temp.set_topic(topic)
		print(temp)
		trends.append(temp)

if __name__ == '__main__':
	main()
