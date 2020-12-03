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

counter = 1
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
        
        time.sleep(2)
        comapnyParticipants = []
        corporateParticipants = []
        executiveParticipants = []
        callParticipants = []
        speech = ""
        QA = 0
        for paragraph in innerPostparagraphs:
            if 'Question-and-Answer Session' or 'Q&A' in paragraph.getText():
                QA = 1
            # print(paragraph.getText())
            if 'Bye' not in paragraph.getText():
                if paragraph.getText() == 'Company Participants':
                    comapnyParticipants = paragraph.find_next_sibling('p').getText()
                    comapnyParticipant = paragraph.find_next_sibling('p')
                    # while time.time() < timeout_start + timeout:
                    while 'Operator' not in comapnyParticipants and 'Conference Call Participants' not in comapnyParticipants and (time.time() < timeout_start + timeout):
                        if comapnyParticipant.find_next_sibling('p') is not None:
                            comapnyParticipants += ', ' + comapnyParticipant.find_next_sibling('p').getText()
                            comapnyParticipant = comapnyParticipant.find_next_sibling('p')
                        else:
                            comapnyParticipants = 'Operator'
                elif paragraph.getText() == 'Corporate Participants':
                    corporateParticipants = paragraph.find_next_sibling('p').getText()
                    corporateParticipant = paragraph.find_next_sibling('p')
                    while 'Operator' not in corporateParticipants and 'Conference Call Participants' not in corporateParticipants and (time.time() < timeout_start + timeout):
                        if corporateParticipant.find_next_sibling('p') is not None:
                            corporateParticipants += ', ' + corporateParticipant.find_next_sibling('p').getText()
                            corporateParticipant = corporateParticipant.find_next_sibling('p')
                        else:
                            corporateParticipants = 'Operator'
                elif paragraph.string == 'Executives':
                    executiveParticipants = paragraph.find_next_sibling('p').getText()
                    executiveParticipant = paragraph.find_next_sibling('p')
                    while 'Operator' not in executiveParticipants and 'Conference Call Participants' not in executiveParticipants and (time.time() < timeout_start + timeout):
                        if executiveParticipant.find_next_sibling('p') is not None:
                            executiveParticipants += ', ' + executiveParticipant.find_next_sibling('p').getText()
                            executiveParticipant = executiveParticipant.find_next_sibling('p')
                        else:
                            executiveParticipants = 'Operator'
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
                elif paragraph.getText() == 'Operator':
                    if paragraph.find_next_sibling('p') is not None:
                        speech = paragraph.find_next_sibling('p').getText()
                        

                if 'Operator' in callParticipants:
                    callParticipants = callParticipants.replace(', Operator','')
                elif 'Operator' in comapnyParticipants:
                    comapnyParticipants = comapnyParticipants.replace(', Operator','')
                elif 'Operator' in corporateParticipants:
                    corporateParticipants = corporateParticipants.replace(', Operator','')
                elif 'Operator' in executiveParticipants:
                    executiveParticipants = executiveParticipants.replace(', Operator','')
                elif 'Conference Call Participants' in comapnyParticipants:
                    comapnyParticipants = comapnyParticipants.replace(', Conference Call Participants','')
                elif 'Conference Call Participants' in corporateParticipants:
                    corporateParticipants = corporateParticipants.replace(', Conference Call Participants','')
                elif 'Conference Call Participants' in executiveParticipants:
                    executiveParticipants = executiveParticipants.replace(', Conference Call Participants','')
            
        
        print(conference_url, comapnyParticipants)

        participant_line=[conference_id,conference_url,comapnyParticipants, corporateParticipants, executiveParticipants, callParticipants, speech, QA]

        with open('rawData-result.csv','a', newline='') as f:
            try:
                writer=csv.writer(f)
                writer.writerow(participant_line)
            except UnicodeEncodeError:
                num_uncoded +=1

        time.sleep(5)
        
        if(len(comapnyParticipants) == 0 and len(corporateParticipants) == 0):
            failedURLs += conference_url 
            counter += 1
            

        if counter > 5:
            with open('rawDataMissing.csv','a', newline='') as f:
                try:
                    writer=csv.writer(f)
                    writer.writerow(failedURLs)
                except UnicodeEncodeError:
                    num_uncoded +=1
        time.sleep(30)
        counter = 0
