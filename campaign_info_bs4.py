from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import getcwd
from lxml import html
import requests
from requests.models import Response
from datetime import datetime, timedelta


def scrape_campaign(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    # list containing all the information (roughly matching Heather's format)
    # [Name, Reason for Fund, Total Raised, Total Requested, Raised Ratio, Link, Date Created, Organizor, Beneficiary, Location, donors, shares, followers]
    information_list = []

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
    extract campaign link
    '''
    information_list.append(url)


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
    extract the organizor of the campaign.
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
            information_list.append(location)
        except:
            #print("No location found")
            information_list.append(float('nan'))

    '''
    extracting dynamic parts of the page: donors, followers, shares
    '''
    driver = webdriver.Chrome(getcwd()+'/chromedriver')
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    try:
        info = soup.find(class_='o-campaign-sidebar-wrapper')
        info = info.text.split('goal')[1]
        donors = int(info.split('donors')[0])
        information_list.append(donors)

        info = info.split('donors')[1]
        shares = int(info.split('shares')[0])
        information_list.append(shares)

        info = info.split('shares')[1]
        followers = int(info.split('followers')[0])
        information_list.append(followers)

    except:
        for i in range(3):
            information_list.append(float('nan'))

    return information_list


# test run
url = "https://www.gofundme.com/f/plrfzw"
campaign_info = scrape_campaign(url)
print(campaign_info)