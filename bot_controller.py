#bot controller

from twitapi import get_trends
from web_scraping import get_articles
from common_trend_detector import get_topics, compare_trends
from text_summarization_module import get_summarized_article
import traceback

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

	def get_tweet(self):
		return self.summarized_articles[0]+' '+self.articles[0].link+' '+self.trend

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
			if articles[i].text=='':
				delete.append(i)
		for i in delete:
			del articles[i]
		if len(articles)==0:
			del temp
			continue

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
		print(temp)
		trends.append(temp)

	for i in range(len(trends)-1):
		for j in range(i+1,len(trends)):
			if compare_trends(trends[i].topic,trends[j].topic):
				print('similar trends')
				del trend[j]

	print('\n\n\n\n\n\n\n')
	print(raw_trends)
	for item in trends:
		print(item.get_tweet())

if __name__ == '__main__':
	main()
