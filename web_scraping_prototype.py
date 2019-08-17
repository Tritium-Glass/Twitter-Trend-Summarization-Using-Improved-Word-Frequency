#web_scraping_prototype

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
from text_sum import make_summary
from bs4 import BeautifulSoup

def main():
	#while True:
	#search = input("Enter an item to search: ")
	search = "hello there"
	search = '+'.join(search.split())
	url = "https://www.bbc.co.uk/search?q="+search+"&filter=news"

	#print(url)
	page = requests.get(url)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib') 
	#print(soup)
	#soup = soup.prettify()
	page_urls = soup.find_all('h1',attrs={'itemprop':"headline"})
	
	links = []
	for page_url in page_urls: 
		children = page_url.findChildren("a" , recursive=False)
		#print(children)
		links.append(children[0]['href'])
	#print(links)
	get_content(links[0])

def get_content(link):
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib') 

	sentence_list = soup.find_all('p')

	text = []
	for sentence in sentence_list:
		text.append(sentence.contents)

	print(text)
	text= ''.join(text)

	print(text,'\n\n\n')
	make_summary(text)

if __name__ == '__main__':
	main()