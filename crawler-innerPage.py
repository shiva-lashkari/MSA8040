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
        conference_url = "https://seekingalpha.com/article/4393034-rgc-resources-inc-rgco-ceo-paul-nester-on-q4-2020-results-earnings-call-transcript"
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
        operator = ""
        QA = 0
        for paragraph in innerPostparagraphs:
            if 'Question-and-Answer Session' in paragraph.getText():
                QA = 1
            # Looking for 'Company Participants' as a title
            if paragraph.getText() == 'Company Participants':
                comapnyParticipant = paragraph.find_next_sibling('p')
                comapnyParticipants = comapnyParticipant.getText()

                while 'Operator' not in comapnyParticipants and 'Conference Call Participants' not in comapnyParticipants \
                    and 'Question-and-Answer' not in comapnyParticipants and (time.time() < timeout_start + timeout):

                    comapnyParticipant = comapnyParticipant.find_next_sibling('p')
                    
                    if comapnyParticipant is not None:
                        search_result = re.search(r'\b' + comapnyParticipant.getText() + 'W', comapnyParticipants)
                        if search_result is None:
                            search_result = ""
                        else:
                            search_result = search_result.group()

                        if comapnyParticipant.getText().replace(" ","") != search_result.replace(" ",""):
                            comapnyParticipants += ', ' + comapnyParticipant.getText()

                        elif comapnyParticipant.getText().replace(" ","") == search_result.replace(" ",""):
                            speechPerson = comapnyParticipant.getText()
                            speech = ""
                            speechTag = comapnyParticipant.find_next_sibling('p')
                            speech = speechTag.getText()
                            
                            speechTag = speechTag.find_next_sibling('p')
                            while speechTag is not None and speechTag.getText() not in comapnyParticipants and \
                                'Question-and-Answer' not in speechTag.getText() and 'Operator' not in speechTag:
                                speech += ', ' + speechTag.getText()
                                speechTag = speechTag.find_next_sibling('p')

                            speech_line=[conference_id,conference_url, speechPerson, speech]

                            with open('rawData-speech.csv','a', newline='') as f:
                                try:
                                    writer=csv.writer(f)
                                    writer.writerow(speech_line)
                                except UnicodeEncodeError:
                                    num_uncoded +=1
                        else:
                            comapnyParticipants += ', Operator'
            elif paragraph.getText() == 'Corporate Participants':
                corporateParticipant = paragraph.find_next_sibling('p')
                corporateParticipants = corporateParticipant.getText()

                while 'Operator' not in corporateParticipants and 'Conference Call Participants' not in corporateParticipants \
                    and (time.time() < timeout_start + timeout):

                    corporateParticipant = corporateParticipant.find_next_sibling('p')

                    if corporateParticipant is not None and corporateParticipant.getText() not in comapnyParticipants:
                        corporateParticipants += ', ' + corporateParticipant.getText()
                    else:
                        corporateParticipants += ', Operator'

            elif paragraph.string == 'Executives':
                executiveParticipant = paragraph.find_next_sibling('p')
                executiveParticipants = executiveParticipant.getText()

                while 'Operator' not in executiveParticipants and 'Conference Call Participants' not in executiveParticipants \
                    and (time.time() < timeout_start + timeout):

                    executiveParticipant = executiveParticipant.find_next_sibling('p')

                    if executiveParticipant is not None and executiveParticipant.getText() not in comapnyParticipants:
                        executiveParticipants += ', ' + executiveParticipant.getText()
                    else:
                        executiveParticipants += ', Operator'

            elif paragraph.string == 'Conference Call Participants':
                callParticipant = paragraph.find_next_sibling('p')
                callParticipants = callParticipant.getText()
                
                while 'Operator' not in callParticipants and 'Conference Call Participants' not in callParticipants \
                    and (time.time() < timeout_start + timeout):

                    callParticipant = callParticipant.find_next_sibling('p')

                    if callParticipant is not None and callParticipant.getText() not in comapnyParticipants:
                        callParticipants += ', ' + callParticipant.getText()
                    else:
                        executiveParticipants += ', Operator'


            elif paragraph.getText() == 'Operator':
                if paragraph.find_next_sibling('p') is not None:
                    operator = paragraph.find_next_sibling('p').getText()
                    

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
            elif 'None' in callParticipants:
                callParticipants = callParticipants.replace(', None','')
    
        # print(conference_url, comapnyParticipants)

        participant_line=[conference_id,conference_url,comapnyParticipants, corporateParticipants, executiveParticipants, callParticipants, operator, QA]
        

        with open('rawData-result.csv','a', newline='') as f:
            try:
                writer=csv.writer(f)
                writer.writerow(participant_line)
            except UnicodeEncodeError:
                num_uncoded +=1
        time.sleep(2)

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

