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

def bbc_search(phrase):

	search = phrase
	search = '+'.join(search.split())
	url = "https://www.bbc.co.uk/search?q="+search+"&filter=news"
    #https://www.bbc.co.uk/search?q=trump&filter=news


	page = requests.get(url)

	soup = BeautifulSoup(page.text, 'html5lib')

	articles = soup.find('ol',attrs={'class':"search-results results"})
	articles_list =articles.find_all('li')

	article_links = []
	for article in articles_list:
		time_text = str(article.find("time").text).lstrip().rstrip()

		article_time = datetime.strptime(time_text,'%d %b %Y').timestamp()
		now = datetime.today().timestamp()

		if now-article_time > 259200:
			continue

		article_link = str(article.find('a',attrs={'class':"rs_touch"}).attrs['href'])


		article_links.append(article_link)

	return article_links

def bbc_webpage_to_text(link):

	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find('div',attrs={'class':"story-body__inner"})

	sentence_list = body_content.find_all('p')

	text = []
	for sentence in sentence_list:
		text.append(sentence.text)

	text= ''.join(text)

	return text

def aljazeera_search(phrase):

	driver = start_browser()

	search = phrase
	search = '+'.join(search.split())

	driver.get("https://www.aljazeera.com/Search/?q="+search)
	#https://www.aljazeera.com/Search/?q=trump
	sleep(20)
	articles = driver.find_elements_by_xpath("//div[@class='row topics-sec-item   ']")

	article_links = []

	for article in articles:
		# print(article.text)
		exact_article = article.find_element_by_xpath("div[@class='col-sm-7 topics-sec-item-cont']")
		article_link = exact_article.find_element_by_xpath("a")
		print(exact_article.text)
		# print(article_link.get_attribute('href'))
		if phrase in article_link.text.lower() and "in pictures" not in article_link.text.lower():
			article_links.append(article_link.get_attribute('href'))

	driver.close()

	return article_links

def aljazeera_webpage_to_text(link):

	#print('a')
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find('div',attrs={'class':"main-article-body"})

	sentence_list = body_content.find_all('p')

	text = []
	article = "".encode("utf-8")
	for sentence in sentence_list:
		text=""
		try:
			text = sentence.find('span').text.encode("utf-8")
		except Exception as e:
			print("no span")

		if len(text)==0:
			text = sentence.text.encode("utf-8")

		article += text

	return str(article)
