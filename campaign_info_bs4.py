from bs4 import BeautifulSoup
from lxml import html
import requests

url = "https://www.gofundme.com/f/gofundmecomf2d58q-grace-grief-and-gabby?qid=9ed142a939566092c4a8774e687a1ec1"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


'''
extract the title of the campaign.
'''
info = soup.find(class_='a-campaign-title')
info = info.text
print("This campaign is titled: " + info)


'''
extract the organizor of the campaign.
'''
info = soup.find(class_='m-campaign-members-main-organizer')
info = info.text
organizer = info.split("Organizer")[0]
print("This campaign is organized by: " + organizer)

'''
extract the location of the campaign.
'''
info = soup.find(class_='m-campaign-members-main-organizer')
info = info.text
location = info.split("Organizer")[1]
print("This campaign is located at: " + location)


'''
extract campaign date
'''
info = soup.find(class_='m-campaign-byline-created a-created-date')
date = info.text[8:]
print("This campaign was created on: " + date)


'''
extract campaign tag
'''
info = soup.find(class_='m-campaign-byline-type divider-prefix meta-divider flex-container align-middle color-dark-gray a-link--unstyled a-link')
tag = info.text
print("This campaign has the tags: " + tag)


'''
extracts the amount raised and the total goal of a campaign.
then calculate how much of the goal was reached in terms of a percentage.
'''
info = soup.find(class_='m-progress-meter-heading')
#print(info.prettify())
info = info.text
amount_raised = info.split("raised")[0]
amount_raised = int(amount_raised[1:].replace(',',''))

try:
    total_goal = info.split("of")[1]
    total_goal = total_goal.split("goal")[0]
    total_goal = int(total_goal[2:].replace(',',''))

    percent_goal_reached = int((amount_raised/total_goal)*100)
    print("This campaign reached " + str(percent_goal_reached) + "% of its goal.")

except:
    print("This campaign raised $" + str(amount_raised) + ". There was no total goal.")




