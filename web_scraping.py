#web_scraping_prototype

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
from datetime import date,datetime
from bs4 import BeautifulSoup
import bs4
import re
import traceback

class article:
	def __init__(self,link,article_age=-1):
		self.link = link
		self.text = ''
		self.article_age = article_age

	def set_text(self,text):
		self.text = text

	def set_upload_time(self,article_age):
		self.article_age = article_age

	def __repr__(self):
		return '\nLink: '+self.link+'\nArticle Age: '+str(self.article_age)+'\nText: '+self.text

def bbc_search(phrase):

	articles = []

	try:
		search = phrase
		search = '+'.join(search.split())
		url = "https://www.bbc.co.uk/search?q="+search+"&filter=news"

		page = requests.get(url)

		soup = BeautifulSoup(page.text, 'html5lib')


		articles_on_page = soup.find('div',attrs={'class':"css-5qhota-Stack e1y4nx260"})
		articles_list = articles_on_page.find_all('div',attrs={'class':"css-16ck4pk-PromoContent ett16tt10"})

		article_links = []
		for item in articles_list:
			try:

				time_span = item.find('span',attrs={'class':"css-1hizfh0-MetadataSnippet ecn1o5v0"})
				time_text = time_span.find_all('span')[1].text

				article_time = datetime.strptime(time_text,'%d %b %Y').timestamp()
				now = datetime.today().timestamp()

				if now-article_time > 259200:
					break

				article_link = str(item.find('a',attrs={'class':"css-rjlb9k-PromoLink ett16tt7"}).attrs['href'])
				if not (re.search(r'\bprogrammes\b',article_link)):

					temp_article = article(article_link,now-article_time)

					articles.append(temp_article)
			except Exception as e:
				print(traceback.format_exc())

	except Exception as e:
		print(traceback.format_exc())
		return []

	return articles

def bbc_webpage_to_text(link):

	try:
		page = requests.get(link)
		#print(page.text[:1000])
		soup = BeautifulSoup(page.text, 'html5lib')

		body_content = soup.find('div',attrs={'class':"story-body__inner"})

		sentence_list = body_content.find_all('p')

		text = []
		for sentence in sentence_list:
			text.append(sentence.text)

		text= ''.join(text)
	except Exception as e:
		print(traceback.format_exc())
		# print(e)
		return ""

	return text

def start_browser():

	dir = os.path.dirname(__file__)
	chrome_driver_path = dir + "/chromedriver.exe"
	chrome_options = Options()
	# "https://www.aljazeera.com/Search/?q="+search
	chrome_options.add_argument("--headless")
	#chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
	# create a new Chrome session

	return webdriver.Chrome(options=chrome_options)

def aljazeera_search(phrase):

	driver = start_browser()

	search = phrase
	search = '+'.join(search.split())

	driver.get("https://www.aljazeera.com/Search/?q="+search)
	#https://www.aljazeera.com/Search/?q=trump
	sleep(20)
	articles_list = driver.find_elements_by_xpath("//div[@class='row topics-sec-item   ']")

	article_links = []
	articles = []

	for item in articles_list:
		# print(article.text)
		try:
			exact_article = item.find_element_by_xpath("div[@class='col-sm-7 topics-sec-item-cont']")
			article_link = exact_article.find_element_by_xpath("a")
			article_time = exact_article.find_element_by_xpath("//span[@class='humanize-datetime']").get_attribute('data-modifieddate')[:-1]

			article_time = datetime.strptime(article_time,'%Y-%m-%dT%H:%M:%S').timestamp()
			now = datetime.today().timestamp()

			if now-article_time > 259200:
				print("skipped")
				break
			if phrase in article_link.text.lower() and "in pictures" not in article_link.text.lower():

				temp_article = article(article_link.get_attribute('href'),now-article_time)
				articles.append(temp_article)
		except Exception as e:
			print(traceback.format_exc())
			continue

	driver.close()

	return articles

def aljazeera_webpage_to_text(link):

	#print('a')
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find('div',attrs={'class':"main-article-body"})

	sentence_list = body_content.find_all('p')

	article = str("".encode("utf-8"))
	for sentence in sentence_list:
		text=""
		try:
			text = sentence.find('span').text.encode("utf-8")
		except Exception as e:
			pass

		if len(text)!=0:
			text = sentence.text.encode("utf-8")

		article += str(text)

	return str(article)

def get_articles(trend):
	articles = []
	bbc_articles = bbc_search(trend)
	for article in bbc_articles:
		text = bbc_webpage_to_text(article.link)

		article.set_text(bbc_webpage_to_text(article.link))

	for article in bbc_articles:

		if len(article.text)!=0:
			#print(article)
			#print(len(article.text))
			articles.append(article)

	aljazeera_articles = aljazeera_search(trend)

	for article in aljazeera_articles:
		text = aljazeera_webpage_to_text(article.link)

		if len(text)==0:
			del article
		else:
			article.set_text(aljazeera_webpage_to_text(article.link))

	for article in aljazeera_articles:
		if len(article.text)!=0:
			#print(article)
			#print(len(article.text))
			articles.append(article)

	return articles

if __name__ == '__main__':
	for article in get_articles('trump'):
		print(article)
