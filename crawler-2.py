import os
from bs4 import BeautifulSoup
import requests
import random
import re
import csv
import time
from datetime import date, timedelta, datetime
from selenium import webdriver

# timeout variable can be omitted, if you use specific value in the while condition
# timeout = 9  # [seconds]

browser = webdriver.Chrome(executable_path = '/home/shiva/myCodes/finalDM/chromedriver')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

timeout = 20
failedURLs = []
with open('rawData.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        timeout_start = time.time()
        participants = []
        # while(len(participants) == 0):
        conference_url = (row[-1])
        conference_id = (row[0])
        browser.get(conference_url)
        html = browser.page_source
        innerSoup = BeautifulSoup(html, "lxml")
        innerPostparagraphs = innerSoup.find_all('p')
        
        time.sleep(5)
        participants = []
        callParticipants = []
        for paragraph in innerPostparagraphs:
            # print(paragraph.getText())
            if 'Bye' not in paragraph.getText():
                if paragraph.getText() == 'Company Participants':
                    participants = paragraph.find_next_sibling('p').getText()
                    participant = paragraph.find_next_sibling('p')
                    # while time.time() < timeout_start + timeout:
                    while 'Operator' not in participants and 'Conference Call Participants' not in participants:
                        if participant.find_next_sibling('p') is not None:
                            participants += ', ' + participant.find_next_sibling('p').getText()
                            participant = participant.find_next_sibling('p')
                        else:
                            participants = 'Operator'
                elif paragraph.getText() == 'Corporate Participants':
                    participants = paragraph.find_next_sibling('p').getText()
                    participant = paragraph.find_next_sibling('p')
                    while 'Operator' not in participants and 'Conference Call Participants' not in participants and (time.time() < timeout_start + timeout):
                        if participant.find_next_sibling('p') is not None:
                            participants += ', ' + participant.find_next_sibling('p').getText()
                            participant = participant.find_next_sibling('p')
                        else:
                            participants = 'Operator'
                elif paragraph.string == 'Executives':
                    participants = paragraph.find_next_sibling('p').getText()
                    participant = paragraph.find_next_sibling('p')
                    while 'Operator' not in participants and 'Conference Call Participants' not in participants and (time.time() < timeout_start + timeout):
                        if participant.find_next_sibling('p') is not None:
                            participants += ', ' + participant.find_next_sibling('p').getText()
                            participant = participant.find_next_sibling('p')
                        else:
                            participants = 'Operator'
                elif paragraph.string == 'Conference Call Participants':
                    callParticipants = paragraph.find_next_sibling('p').getText()
                    callParticipant = paragraph.find_next_sibling('p')
                    while 'Operator' not in callParticipants and 'Question-and-Answer Session' not in callParticipants and (time.time() < timeout_start + timeout):
                        try:
                            callParticipants += ', ' + callParticipant.find_next_sibling('p').getText()
                        except:
                            callParticipants +=', None'
                        try:
                            callParticipant = callParticipant.find_next_sibling('p')
                        except:
                            callParticipant ='None'

            if 'Operator' in callParticipants:
                callParticipants = callParticipants.replace(', Operator','')
            elif 'Conference Call Participants' in participants:
                participants = participants.replace(', Conference Call Participants','')
            print(2)
            
        print(conference_url,participants)
        
        if(len(participants) == 0):
            failedURLs += conference_url 
            # data = {
            #     'text': 'slashkari @student.gsu.edu'
            # }
            # with requests.Session() as s:
            #     response = requests.post(url , data)
            #     print(response.text)
            time.sleep(10)
                    
        participant_line=[conference_id,conference_url,participants,callParticipants]
        

        with open('rawData2.csv','a', newline='') as f:
            try:
                writer=csv.writer(f)
                writer.writerow(participant_line)
            except UnicodeEncodeError:
                num_uncoded +=1

        time.sleep(5)
    with open('rawData3.csv','a', newline='') as f:
        try:
            writer=csv.writer(f)
            writer.writerow(failedURLs)
        except UnicodeEncodeError:
            num_uncoded +=1
