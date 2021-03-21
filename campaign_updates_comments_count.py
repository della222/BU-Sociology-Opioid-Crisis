from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
from os import getcwd
from bs4 import BeautifulSoup
import requests

PATH = getcwd() + '/chromedriver'
driver = webdriver.Chrome(PATH)

def get_updatecomment_count(urls):
    '''
    get_updatecomment_count(): this function takes a URL for a GoFundMe campaign and returns 
    the number of campaign comments & updates if applicable 
    
    Args:
        urls (list of strings): list of GoFundMe urls

    Returns:
        num_updates (list of ints): list of # of campaign updates
        num_comments (list of ints): list of # of campaign comments
    '''
    num_updates = []
    num_comments = []
    for url in urls:
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom of GoFundMe page
        time.sleep(3) # wait for updates and comments section to load

        html = driver.page_source
        parsed_html = BeautifulSoup(html, features="lxml") # parse HTML from Chromedriver
        driver.close()

        updates = parsed_html.find('div', class_='p-campaign-updates')
        comments = parsed_html.find('div', class_='p-campaign-comments')

        num_updates.append(0) if updates == None else num_updates.append(int(re.sub("[^0-9]", "", updates.h2.text))) # regex to remove text, keep only updates as number
        num_comments.append(0) if comments == None else num_comments.append(int(re.sub("[^0-9]", "", comments.h2.text))) # regex remove text, keep only comments as number
    return num_updates, num_comments

urls = ["https://www.gofundme.com/f/whose-corner-is-it-anyway?qid=30352514c51c3880fb30bc9429c27736", "https://www.gofundme.com/f/1wlddigtio?qid=067af41e16867d4d13a291ad6df401d0", "https://www.gofundme.com/f/stop-kenney-from-shutting-down-ioat?qid=a64ddf83d13463c4b63db182661b2c1e", "https://www.gofundme.com/f/pups-need-veterinary-care-amp-family-help?qid=90c8529e6c4593f41a1916048b306c2c"]
print(get_updatecomment_count(urls))