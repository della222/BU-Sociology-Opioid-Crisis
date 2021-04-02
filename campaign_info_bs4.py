from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import getcwd
from lxml import html
import requests
from requests.models import Response
from datetime import datetime, timedelta
import json
import re
from time import time, sleep
import pandas as pd
import numpy as np
import random
from urllib.request import Request
from os import getcwd

URLPATH = getcwd() + '/data/urls.csv'
cols = [
    'URL',
    'All_Keywords',
    'Title',
    'Reason_For_Fund',
    'Total_Raised',
    'Total_Goal',
    'Percent_Reached',
    'Campaign_Date',
    'Organizer',
    'Beneficiary',
    'Location',
    'Donors',
    'Shares',
    'Followers',
    'Num_Updates',
    'Num_Comments',
    "Is_Charity",
    "Charity", "Currency_Code", "Donation_Count", "Comments_Enabled", "Donations_Enabled", "Country", "Is_Business", "Is_Team", "Campaign_Photo_URL", "Description"
]

def scrape_campaign(url_row):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    page = requests.get(url_row[0], headers={'User-Agent': user_agent})
    sleep(random.uniform(3,5))
    soup = BeautifulSoup(page.text, "lxml")

    # list containing all the information (roughly matching Heather's format)
    # [Name, Reason for Fund, Total Raised, Total Requested, Raised Ratio, Date Created, Organizer, Beneficiary, Location]
    information_list = [url_row[0], reformat_keyword_list(url_row[1])]

    '''
    extract the title of the campaign.
    '''
    try:
        info = soup.find(class_='a-campaign-title')
        title = info.text
        #print("This campaign is titled: " + title)
        information_list.append(title)
    except:
        #print("No title found")
        information_list.append(float('nan'))


    '''
    extract campaign tag, which tells the reason for campaign
    '''
    try:
        info = soup.find(class_='m-campaign-byline-type divider-prefix meta-divider flex-container align-middle color-dark-gray a-link--unstyled a-link')
        tag = info.text
        #print("This campaign has the tags: " + tag)
        information_list.append(tag)
    except:
        #print("No tags found")
        information_list.append(float('nan'))


    '''
    extracts the amount raised
    '''
    try:
        info = soup.find(class_='m-progress-meter-heading')
        info = info.text
        amount_raised = info.split(" raised")[0]
        amount_raised = int(amount_raised[1:].replace(',',''))
        information_list.append(amount_raised)
    except:
        information_list.append(float('nan'))

    '''
    extracts the total goal of a campaign.
    then calculate how much of the goal was reached in terms of a percentage.
    '''
    try:
        info = soup.find(class_='m-progress-meter-heading')
        info = info.text
        total_goal = info.split("of")[1]
        total_goal = total_goal.split("goal")[0]
        total_goal = int(total_goal[2:].replace(',',''))

        percent_goal_reached = round((amount_raised/total_goal), 2)
        #print("This campaign reached " + str(percent_goal_reached) + "% of its goal.")
        information_list.append(total_goal)
        information_list.append(percent_goal_reached)
    except:
        #print("This campaign raised $" + str(amount_raised) + ". There was no total goal.")
        information_list.append(float('nan'))
        information_list.append(float('nan'))

    '''
    extract date that campaign was created
    '''
    try:
        info = soup.find(class_='m-campaign-byline-created a-created-date')
        days_ago = info.text.split("days ago")[0]
        days_ago = int(days_ago[len("Created "):])

        date_created = datetime.date(datetime.now()) - timedelta(days=days_ago)
        date_created = date_created.strftime('%B %d, %Y')
        information_list.append(date_created)
    except:
        try:
            info = soup.find(class_='m-campaign-byline-created a-created-date')
            date = info.text[len("Created "):]
            #print("This campaign was created on: " + date)
            information_list.append(date)
        except:
            #print("No date found")
            information_list.append(float('nan'))


    '''
    extract the organizer of the campaign.
    '''
    try:
        info = soup.find(class_='m-campaign-members-main-organizer')
        organizer = info.text.split("Organizer")[0]
        organizer = organizer.replace(u'\xa0', u'')
        #print("This campaign is organized by: " + organizer)
        information_list.append(organizer)
    except:
        #print("No organizer found")
        information_list.append(float('nan'))


    '''
    extract the beneficiary of the campaign.
    '''
    try:
        info = soup.find(class_='m-campaign-byline-description')
        beneficiary = info.text.split("behalf of ")[1][:-1]
        #print("This campaign is created to help: " + beneficiary)
        information_list.append(beneficiary)
    except:
        try:
            info = soup.find(class_='m-campaign-byline-description')
            beneficiary = info.text.split("benefit ")[1][:-1]
            #print("This campaign is created to help: " + beneficiary)
            information_list.append(beneficiary)
        except:
            #print("No beneficiary found")
            information_list.append(float('nan'))


    '''
    extract the location of the campaign.
    '''
    try:
        info = soup.find(class_='m-campaign-members-main-organizer')
        location = info.text.split("donations")[1]
        #print("This campaign is located at: " + location)
        information_list.append(location)
    except:
        try:
            location = info.text.split("Organizer")[1]
            #print("This campaign is located at: " + location)
            information_list.append(location) if location != '' else information_list.append(float('nan'))
        except:
            #print("No location found")
            information_list.append(float('nan'))

    '''
    extracting dynamic parts of the page: donors, followers, shares
    reference: https://stackoverflow.com/questions/35613024/convert-number-from-15-5k-and-1-20m-to-15-500-and-1-200-000-python
    '''
    driver = webdriver.Chrome(getcwd()+'/chromedriver')
    driver.get(url_row[0])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom of GoFundMe page
    # sleep(3)
    try: # wait for HTML list containing donors, shares, followers, info to load  
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-unstyled m-meta-list m-meta-list--default')))
        # print ("Loaded")
    except TimeoutException:
        # print ("Timeout")
        pass 
    
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    # info = soup.find(class_='o-campaign-sidebar-wrapper')

    # info = info.text.split()
    # print(info)
    # donors = info[4].replace('goal', '')
    # shares = info[5].replace('donors', '')
    # followers = info[6].replace('shares', '')
    # try:
    #     shares = float(shares)  
    # except ValueError:
    #     unit = shares[-1]                 
    #     shares = float(shares[:-1])        
    #     shares = (shares * units[unit])

    # print(donors, shares, followers)

    try:
        units = {"K":1000,"M":1000000} # conversion shorthand number format (1K) to float representation (1000.0)
        info = soup.find(class_='o-campaign-sidebar-wrapper')
        info = info.text.split()
        donors = info[4].replace('goal', '')
        try: # does not contain K, M
            donors = float(donors)
            information_list.append(donors)  
        except: # contains K, M
            unit = donors[-1]                 
            donors = float(donors[:-1])        
            donors = (donors * units[unit]) # turn 1K into 1000
            information_list.append(donors)
    except:
        information_list.append(float('nan'))

    try:
        units = {"K":1000,"M":1000000} 
        info = soup.find(class_='o-campaign-sidebar-wrapper')
        info = info.text.split()
        shares = info[5].replace('donors', '')
        try:
            shares = float(shares) 
            information_list.append(shares)
        except ValueError:
            unit = shares[-1]                 
            shares = float(shares[:-1])        
            shares = (shares * units[unit])
            information_list.append(shares)
    except:
        information_list.append(float('nan'))

    try:
        units = {"K":1000,"M":1000000} 
        info = soup.find(class_='o-campaign-sidebar-wrapper')
        info = info.text.split()
        followers = info[6].replace('shares', '')
        try:
            followers = float(followers) 
            information_list.append(followers)
        except ValueError:
            unit = followers[-1]                 
            followers = float(followers[:-1])        
            followers = (followers * units[unit])
            information_list.append(followers)
    except:
        information_list.append(float('nan'))
    
    '''
    get # of campaign updates
    '''
    try:
        info = soup.find('div', class_='p-campaign-updates')
        information_list.append(0) if info.text == None else information_list.append(int(re.sub("[^0-9]", "", info.h2.text))) # regex remove text, keep only updates number
    except:
        information_list.append(float('nan'))

    '''
    get # of campaign comments
    '''
    try:
        info = soup.find('div', class_='p-campaign-comments')
        information_list.append(0) if info.text == None else information_list.append(int(re.sub("[^0-9]", "", info.h2.text))) # regex remove text, keep only updates number
    except:
        information_list.append(float('nan'))


    # except:
    #     for i in range(3):
    #         information_list.append(float('nan'))

    '''
    extract information stored in JSON format inside the page's window\.initialState script tag 

    is_charity_data (bool): where True if campaign is a charity, False if not
    charity_data (string): charity name if provided
    currency_code_data (string): campaign currency code
    donation_count_data (int): amount of campaign donations
    comments_enabled_data (bool): True if campaign has comments enabled, False if not
    donations_enabled_data (bool): True if campaign has donations enabled, False if not
    has_donations_data (bool): True if campaign has donations, False if not
    country_data (string): country code
    is_business_data (bool): True if campaign is business, False if not
    is_team_data (bool): True if campaign has team, False if not
    '''
    
    html = page.text
    try:
        data = json.loads(re.findall(r'window\.initialState = ({.*?});', html)[0]) #output "initialState" script that contains campaign info
    except:
        pass

    try:
        is_charity_data = data['feed']['campaign']['is_charity']
        information_list.append(is_charity_data)
    except:
        information_list.append(float('nan'))

    try: 
        charity_data = data['feed']['campaign']['charity']
        information_list.append(charity_data) if charity_data != {} else information_list.append(float('nan'))
    except:
        information_list.append(float('nan'))
    
    try:
        currency_code_data = data['feed']['campaign']['currencycode']
        information_list.append(currency_code_data)
    except:
        information_list.append(float('nan'))

    try:
        donation_count_data = int(data['feed']['campaign']['donation_count'])
        information_list.append(donation_count_data)
    except:
        information_list.append(float('nan'))

    try:
        comments_enabled_data = data['feed']['campaign']['comments_enabled']
        information_list.append(comments_enabled_data)
    except:
        information_list.append(float('nan'))

    try:
        donations_enabled_data = data['feed']['campaign']['donations_enabled']
        information_list.append(donations_enabled_data)
    except:
        information_list.append(float('nan'))
    
    try:
        country_data =  data['feed']['campaign']['location']['country']
        information_list.append(country_data)
    except:
        information_list.append(float('nan'))
    
    try:
        is_business_data = data['feed']['campaign']['is_business']
        information_list.append(is_business_data)
    except:
        information_list.append(float('nan'))
    
    try:
        is_team_data = data['feed']['campaign']['is_team']
        information_list.append(is_team_data)
    except:
        information_list.append(float('nan'))
    
    try:
        campaign_photo_data = data['feed']['campaign']['campaign_image_url']
        information_list.append(campaign_photo_data)
    except:
        information_list.append(float('nan'))


    '''
    get campaign description
    '''
    try:
        info = soup.find(class_='o-campaign-description')
        description = info.text
        description = description.replace(u'\xa0', u'')
        information_list.append(description)
    except:
        information_list.append(float('nan'))

    # TESTING
    if (len(information_list) == 27):
        print(information_list)
        print(len(information_list))

    else:
        print(information_list)
        print(len(information_list), "BAD_LENGTH")

    return information_list



def reformat_keyword_list(keywords):
    """
    Converts string version of keywords list back to a python list

    Args:
        keywords (string): Keyword list as one string

    Returns:
        [list]: Python list of each keyword separated into strings
    """    
    kw = keywords.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
    kw = kw.split(",")
    return list(set(kw))


def generate_df(url_csv):
    """
    Calls scraper on each row of url dataframe and returns scraped data

    Args:
        url_csv ([DataFrame]): csv with all urls

    Returns:
        [DataFrame]: scraped data
    """    
    # test with number of urls
    data = pd.DataFrame(url_csv.apply(scrape_campaign, axis=1).tolist(), columns=cols)
    return data


def main():
    start = time()

    # import csv with urls
    url_csv = pd.read_csv(URLPATH)
    print(np.shape(url_csv))

    #url_csv = url_csv[url_csv['urls'] == "https://www.gofundme.com/f/whose-corner-is-it-anyway"]
    data = generate_df(url_csv)
    data.to_csv(getcwd() + '/data/campaign_bs4_data.csv', index=False)
    end = time()
    print(f'Time to run: {(end - start) / 60} minutes')

if __name__ == '__main__':
    main()

