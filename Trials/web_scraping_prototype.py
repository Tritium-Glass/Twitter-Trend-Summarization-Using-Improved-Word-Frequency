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

	try:
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
	except Exception as e:
		return []

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
	#chrome_options.add_argument("--headless")
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
	articles = driver.find_elements_by_xpath("//div[@class='row topics-sec-item   ']")

	article_links = []

	for article in articles:
		# print(article.text)
		exact_article = article.find_element_by_xpath("div[@class='col-sm-7 topics-sec-item-cont']")
		article_link = exact_article.find_element_by_xpath("a")

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
		article_time = link.find_all('span')[4]['rodate']
		article_time = datetime.strptime(article_time,'%Y-%m-%dT%H:%M:%SZ').timestamp()
		now = datetime.today().timestamp()

		if now-article_time > 259200:
			print('skipped')
			break

		links.append("https://timesofindia.indiatimes.com"+link['href'])

	return links
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
		return 'Error'

	return text

if __name__ == '__main__':
	# bbc_articles = bbc_search('trump')
	# for article in bbc_articles:
	# 	print(article)
	# 	print(bbc_webpage_to_text(article))

	# aljazeera_articles = aljazeera_search('trump')
	# for article in aljazeera_articles:
	# 	print(article)
	# 	print(aljazeera_webpage_to_text(article))

	links = toi_search('holi')
	for link in links:
		print(link)
		print(toi_webpage_to_text(link))
