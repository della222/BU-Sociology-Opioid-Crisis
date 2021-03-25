from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from os import getcwd

driver = webdriver.Chrome(getcwd()+'/chromedriver')

campaign = 'https://www.gofundme.com/f/Fentanyl-Testing?qid=c92ee8440e8f330604127a6c642a9de6'
driver.get(campaign)


'''
extract the title of the campaign.
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/header/h1')
info = info.text
print("This campaign is titled: " + info)


'''
extract the organizor of the campaign.
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[3]/div[1]/div/div')
info = info.text
try:
    organizor = info.split("are")[0]
    organizor = organizor.split("FUNDRAISER\n")[1]
except:
    try:
        organizor = info.split("is")[0]
    except:
        print("Organizor not found")

print("This campaign is organized by: " + organizor)


'''
extract campaign date
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[4]/ul/li[1]/span')
date = info.text[8:]
print("This campaign was created on: " + date)

'''
extract number of donors
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[2]/ul/li[1]/button/span[1]')
donors = int(info.text)
print("Number of donors: " + str(donors))

'''
extract number of shares.
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[2]/ul/li[2]/span/span[1]')
shares = int(info.text)
print("Number of shares: " + str(shares))


'''
extract number of followers.
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[2]/ul/li[3]/span/span[1]')
followers = int(info.text)
print("Number of followers: " + str(followers))


'''
extracts the amount raised and the total goal of a campaign.
then calculate how much of the goal was reached in terms of a percentage.
'''
info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[1]/h2')
info = info.text

amount_raised = info.split("raised")[0]
amount_raised = int(amount_raised[1:].replace(',',''))

total_goal = info.split("of")[1]
total_goal = total_goal.split("goal")[0]
total_goal = int(total_goal[2:].replace(',',''))

percent_goal_reached = int((amount_raised/total_goal)*100)
print("This campaign reached " + str(percent_goal_reached) + "% of its goal.")