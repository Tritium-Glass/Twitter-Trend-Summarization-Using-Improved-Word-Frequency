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
	sleep(20)
	articles = driver.find_elements_by_xpath("//div[@class='row topics-sec-item   ']")

	article_links = []

	for article in articles:
		# print(article.text)
		exact_article = article.find_element_by_xpath("div[@class='col-sm-7 topics-sec-item-cont']")
		article_link = exact_article.find_element_by_xpath("a")
		# print(exact_article.text)
		# print(article_link.get_attribute('href'))
		if phrase in article_link.text.lower() and "in pictures" not in article_link.text.lower():
			article_links.append(article_link.get_attribute('href'))

	article_links = article_links[:10]

	driver.close()

	#print(article_links)

	articles_list = []
	for article_link in article_links:
		articles_list.append(aljazeera_webpage_to_text(article_link))
	# cnn_webpage_to_text(article_links[0])

	return articles_list

def aljazeera_webpage_to_text(link):

	#print('a')
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find('div',attrs={'class':"article-p-wrapper"})

	sentence_list = body_content.find_all('p')

	text = []
	for sentence in sentence_list:
		#print(sentence)
		if isinstance(sentence.contents[0],bs4.element.NavigableString):
			text.append(sentence.contents[0])

	# print(text)
	text= ''.join(text)

	try:
		# print(text,'\n')
		return text
	except Exception as e:
		print('error')
		pass

def toi_search(phrase):

	#while True:
	#search = input("Enter an item to search: ")
	search = phrase
	search = '+'.join(search.split())
	url = "https://timesofindia.indiatimes.com/topic/"+search+"/news"

	#print(url)
	page = requests.get(url)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	list_of_articles = soup.find_all('li',attrs={'class':"article"})

	links =[]

	for item in list_of_articles:

		link = item.find('a')
		links.append("https://timesofindia.indiatimes.com"+link['href'])

	for link in links:
		toi_webpage_to_text(link)

	# toi_webpage_to_text(links[0])

def toi_webpage_to_text(link):

	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	sentence_list = []
	text = []

	try:
		body_content = soup.find('div',attrs={'class':"Normal"})

		start_end = [body_content.contents[0],body_content.contents[-1]]
		sentence_list = body_content.find_all('p')

		if len(sentence_list)==0:
			raise Exception

		for sentence in sentence_list:
			#print(sentence)
			if isinstance(sentence.contents[0],bs4.element.NavigableString):
				text.append(sentence.contents[0])
	except Exception as e:
		#print(e)
		return

	# print(text)
	try:
		text= start_end[0]+''.join(text)+start_end[1]

		if len(text)>200:
			print(text,"\n\n\n\n\n")
		# print()
	except Exception as e:
		pass

if __name__ == '__main__':
	bbc_articles = bbc_search('trump')
	for article in bbc_articles:
		print(article)
		print(bbc_webpage_to_text(article))
