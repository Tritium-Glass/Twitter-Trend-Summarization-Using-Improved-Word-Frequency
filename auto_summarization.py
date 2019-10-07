#Automatically sumarizes documents using Resoomer

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

def start_browser():

    dir = os.path.dirname(__file__)
    chrome_driver_path = dir + "/chromedriver.exe"
    chrome_options = Options()
    # "https://www.aljazeera.com/Search/?q="+search
    # chrome_options.add_argument("--headless")
    #chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    # create a new Chrome session

    return webdriver.Chrome(options=chrome_options)

def get_summary(article):

    driver = start_browser()

    try:
        driver.get("https://resoomer.com/en/")
        sleep(5)
        text_area = driver.find_element_by_id('contentText')
        text_area.send_keys(article)
        resoomer_button = driver.find_element_by_id('btnSendText_V2')
        sleep(10)
        try:
            driver.find_element_by_id('arrowTop').click()
        except Exception as e:
            pass
        sleep(2)
        resoomer_button.click()

        article_links = []
        sleep(5)


        result = driver.find_element_by_id('conteneurTextAuto')

        spans = result.find_elements_by_tag_name('span')
        result = result.text
        # for item in spans:
        #     result += item.text

        print(result)

        return result
    except Exception as e:
        print(e)
        sleep(10)
    finally:
        driver.close()

def main():
    get_summary("Microsoft held talks in the past few weeks to acquire software developer platform GitHub, Business Insider reports. One person familiar with the discussions between the companies told CNBC that they had been considering a joint marketing partnership valued around $35 million, and that those discussions had progressed to a possible investment or outright acquisition. It is unclear whether talks are still ongoing, but this person said that GitHub's price for a full acquisition was more than Microsoft currently wanted to pay. GitHub was last valued at $2 billion in its last funding round 2015, but the price tag for an acquisition could be $5 billion or more, based on a price that was floated last year. GitHub's tools have become essential to software developers, who use it to store code, keep track of updates and discuss issues. The privately held company has more than 23 million individual users in more than 1.5 million organizations. It was on track to book more than $200 million in subscription revenue, including more than $110 million from companies using its enterprise product, GitHub told CNBC last fall.Microsoft has reportedly flirted with buying GitHub in the past, including in 2016, although GitHub denied those reports. A partnership would give Microsoft another connection point to the developers it needs to court to build applications on its various platforms, including the Azure cloud. Microsoft could also use data from GitHub to improve its artificial intelligence producs. The talks come amid GitHub's struggle to replace CEO and founder Chris Wanstrath, who stepped down 10 months ago. Business Insider reported that Microsoft exec Nat Friedman -- who previously ran Xamarin, a developer tools start-up that Microsoft acquired in 2016 -- may take that CEO role. Google's senior VP of ads and commerce, Sridhar Ramaswamy, has also been in discussions for the job, says the report. Microsoft declined to comment on the report. GitHub did not immediately return a request for comment.")

if __name__ == '__main__':
    main()
