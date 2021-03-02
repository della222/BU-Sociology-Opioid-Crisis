from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/dellalalala/Downloads/chromedriver')

'''
This code extracts the amount raised and the total goal of a campaign.
Then, it calculates how much of the goal was reached in terms of a percentage.
'''

campaign = 'https://www.gofundme.com/f/Fentanyl-Testing?qid=c92ee8440e8f330604127a6c642a9de6'
driver.get(campaign)

info = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[1]/h2')
info = info.text

amount_raised = info.split("raised")[0]
amount_raised = int(amount_raised[1:].replace(',',''))

total_goal = info.split("of")[1]
total_goal = total_goal.split("goal")[0]
total_goal = int(total_goal[2:].replace(',',''))

percent_goal_reached = int((amount_raised/total_goal)*100)
print("This campaign reached " + str(percent_goal_reached) + "% of its goal.")