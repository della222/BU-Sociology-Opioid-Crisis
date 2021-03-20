from bs4 import BeautifulSoup
from lxml import html
import requests
from requests.models import Response

url = "https://www.gofundme.com/f/patrick-h-forsyth-memorial-fund?qid=8a411347885c907a941735de3c5d135d"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


'''
extract the title of the campaign.
'''
try:
    info = soup.find(class_='a-campaign-title')
    title = info.text
    print("This campaign is titled: " + title)
except:
    print("No title found")

'''
extract the organizor of the campaign.
'''
try:
    info = soup.find(class_='m-campaign-members-main-organizer')
    organizer = info.text.split("Organizer")[0]
    print("This campaign is organized by: " + organizer)
except:
    print("No organizer found")


'''
extract the beneficiary of the campaign.
'''
try:
    info = soup.find(class_='m-campaign-byline-description')
    beneficiary = info.text.split("behalf of ")[1][:-1]
    print("This campaign is created to help: " + beneficiary)
except:
    try:
        info = soup.find(class_='m-campaign-byline-description')
        beneficiary = info.text.split("benefit ")[1][:-1]
        print("This campaign is created to help: " + beneficiary)
    except:
        print("No beneficiary found")


'''
extract the location of the campaign.
'''
try:
    info = soup.find(class_='m-campaign-members-main-organizer')
    location = info.text.split("donations")[1]
    print("This campaign is located at: " + location)
except:
    try:
        location = info.text.split("Organizer")[1]
        print("This campaign is located at: " + location)
    except:
        print("No location found")

'''
extract date that campaign was created
'''
try:
    info = soup.find(class_='m-campaign-byline-created a-created-date')
    date = info.text[len("Created "):]
    print("This campaign was created on: " + date)
except:
    print("No date found")

'''
extract campaign tag
'''
try:
    info = soup.find(class_='m-campaign-byline-type divider-prefix meta-divider flex-container align-middle color-dark-gray a-link--unstyled a-link')
    tag = info.text
    print("This campaign has the tags: " + tag)
except:
    print("No tags found")

'''
extracts the amount raised and the total goal of a campaign.
then calculate how much of the goal was reached in terms of a percentage.
'''
info = soup.find(class_='m-progress-meter-heading')
info = info.text
amount_raised = info.split(" raised")[0]
amount_raised = int(amount_raised[1:].replace(',',''))

try:
    total_goal = info.split("of")[1]
    total_goal = total_goal.split("goal")[0]
    total_goal = int(total_goal[2:].replace(',',''))

    percent_goal_reached = int((amount_raised/total_goal)*100)
    print("This campaign reached " + str(percent_goal_reached) + "% of its goal.")

except:
    print("This campaign raised $" + str(amount_raised) + ". There was no total goal.")
