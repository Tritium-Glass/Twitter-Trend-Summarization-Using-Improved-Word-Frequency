import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
from bs4 import BeautifulSoup
import bs4

def start_browser():

    dir = os.path.dirname(__file__)
    chrome_driver_path = dir + "/chromedriver.exe"
    chrome_options = Options()
    # "https://www.aljazeera.com/Search/?q="+search
    #chrome_options.add_argument("--headless")
    #chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    # create a new Chrome session

    return webdriver.Chrome(options=chrome_options)

def bbc_search(phrase):
    #while True:
    #search = input("Enter an item to search: ")
    search = phrase
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
    bbc_webpage_to_text(links[2])

def bbc_timeline_search(phrase):

    driver = start_browser()

    search = '+'.join(phrase.split())

    driver.get("https://www.bbc.co.uk/search?q="+search+"&filter=news")
    sleep(5)

    try:
        for i in range(1):
            driver.find_element_by_xpath('//*[@id="search-content"]/nav[1]/a').click()
            sleep(3)
            article_bunches = driver.find_elements_by_tag_name('ol')
    except Exception as e:
        try:
            driver.find_element_by_xpath('//*[@id="search-content"]/nav[1]/a').click()
            sleep(3)
        except Exception as e:
            pass

    sleep(20)

    articles = driver.find_elements_by_tag_name("article")

    article_links = []

    for article in articles:
        # print(article.text)
        time = article.find_element_by_tag_name("time").get_attribute('datetime')
        article_link = article.find_element_by_xpath("a")
        # print(exact_article.text)
        # print(article_link.get_attribute('href'))
        article_links.append([time,article_link.get_attribute('href')])

    driver.close()

    #print(article_links)
    for item in article_links:
        print(item)

    # return articles_list

def bbc_webpage_to_text(link):
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
    bbc_timeline_search('huawei')
