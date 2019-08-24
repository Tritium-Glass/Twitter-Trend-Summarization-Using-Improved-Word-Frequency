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
	print(links)
	get_content(links[2])

def get_content(link):
	print(link)
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find_all('div',attrs={'property':"articleBody"})

	#print(body_content)

	sentence_list = body_content[0].find_all('p')
	print(sentence_list)
	video_check = soup.find_all('video')
	print(video_check)
	if len(video_check)>0:
		print("This is a video based article")
		quit()

	text = []
	for sentence in sentence_list:
		text.append(sentence.contents[0])

	print(text)
	text= ''.join(text)

	print(text,'\n\n\n')
	#make_summary(text)

if __name__ == '__main__':
	main()
