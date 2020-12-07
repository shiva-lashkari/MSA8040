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
        operator = ""
        QA = 0
        for paragraph in innerPostparagraphs:
            if 'Question-and-Answer Session' in paragraph.getText():
                QA = 1
            # Looking for 'Company Participants' as a title
            if paragraph.getText() == 'Company Participants':
                comapnyParticipant = paragraph.find_next_sibling('p')
                comapnyParticipants = comapnyParticipant.getText()
                comapnyParticipant = comapnyParticipant.find_next_sibling('p')

                while 'Conference Call Participants' not in comapnyParticipants \
                    and 'Question-and-Answer' not in comapnyParticipant.getText() and (time.time() < timeout_start + timeout):
                    
                    if comapnyParticipant is not None:
                        search_result = re.search(r'\b' + comapnyParticipant.getText() + '\W', comapnyParticipants)
                        if search_result is None:
                            search_result = ""
                        else:
                            search_result = search_result.group()

                        if comapnyParticipant.getText().replace(" ","") != search_result.replace(" ",""):
                            comapnyParticipants += ', ' + comapnyParticipant.getText()
                            comapnyParticipant = comapnyParticipant.find_next_sibling('p')

                        elif comapnyParticipant.getText().replace(" ","") == search_result.replace(" ","") or \
                            comapnyParticipant.getText() == 'Operator':
                    
                            speechPerson = comapnyParticipant.getText()
                            speech = ""
                            comapnyParticipant = comapnyParticipant.find_next_sibling('p')
                            speech = comapnyParticipant.getText()
                            comapnyParticipant = comapnyParticipant.find_next_sibling('p')

                            while comapnyParticipant is not None and comapnyParticipant.getText().replace(" ","") != search_result.replace(" ","") \
                                and 'Question-and-Answer' not in comapnyParticipant.getText() and 'Operator' not in comapnyParticipant:
                                speech += ', ' + comapnyParticipant.getText()
                                comapnyParticipant = comapnyParticipant.find_next_sibling('p')
                                if comapnyParticipant is not None:
                                    search_result = re.search(r'\b' + comapnyParticipant.getText() + '\W', comapnyParticipants)
                                    if search_result is None:
                                        search_result = ""
                                    else:
                                        search_result = search_result.group()

                            
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
                corporateParticipant = corporateParticipant.find_next_sibling('p')

                while 'Conference Call Participants' not in corporateParticipants \
                    and 'Question-and-Answer' not in corporateParticipant.getText() and (time.time() < timeout_start + timeout):
                    
                    if corporateParticipant is not None:
                        search_result = re.search(r'\b' + corporateParticipant.getText() + '\W', corporateParticipants)
                        if search_result is None:
                            search_result = ""
                        else:
                            search_result = search_result.group()

                        if corporateParticipant.getText().replace(" ","") != search_result.replace(" ",""):
                            corporateParticipants += ', ' + corporateParticipant.getText()
                            corporateParticipant = corporateParticipant.find_next_sibling('p')

                        elif corporateParticipant.getText().replace(" ","") == search_result.replace(" ",""):
                            # print(corporateParticipant)
                            speechPerson = corporateParticipant.getText()
                            speech = ""
                            corporateParticipant = corporateParticipant.find_next_sibling('p')
                            speech = corporateParticipant.getText()
                            corporateParticipant = corporateParticipant.find_next_sibling('p')

                            while corporateParticipant is not None and corporateParticipant.getText().replace(" ","") != search_result.replace(" ","") \
                                and 'Question-and-Answer' not in corporateParticipant.getText() and 'Operator' not in corporateParticipant:
                                speech += ', ' + corporateParticipant.getText()
                                corporateParticipant = corporateParticipant.find_next_sibling('p')
                                if corporateParticipant is not None:
                                    search_result = re.search(r'\b' + corporateParticipant.getText() + '\W', corporateParticipants)
                                    if search_result is None:
                                        search_result = ""
                                    else:
                                        search_result = search_result.group()

                            
                            speech_line=[conference_id,conference_url, speechPerson, speech]

                            with open('rawData-speech.csv','a', newline='') as f:
                                try:
                                    writer=csv.writer(f)
                                    writer.writerow(speech_line)
                                except UnicodeEncodeError:
                                    num_uncoded +=1
                        else:
                            corporateParticipants += ', Operator'

            elif paragraph.string == 'Executives':
                executiveParticipant = paragraph.find_next_sibling('p')
                executiveParticipants = executiveParticipant.getText()
                executiveParticipant = executiveParticipant.find_next_sibling('p')

                while 'Conference Call Participants' not in executiveParticipants \
                    and 'Question-and-Answer' not in executiveParticipant.getText() and (time.time() < timeout_start + timeout):
                    
                    if executiveParticipant is not None:
                        search_result = re.search(r'\b' + executiveParticipant.getText() + '\W', executiveParticipants)
                        if search_result is None:
                            search_result = ""
                        else:
                            search_result = search_result.group()

                        if executiveParticipant.getText().replace(" ","") != search_result.replace(" ",""):
                            executiveParticipants += ', ' + executiveParticipant.getText()
                            executiveParticipant = executiveParticipant.find_next_sibling('p')

                        elif executiveParticipant.getText().replace(" ","") == search_result.replace(" ","") or \
                            executiveParticipant.getText() == 'Operator':
                            # print(executiveParticipant)
                            speechPerson = executiveParticipant.getText()
                            speech = ""
                            executiveParticipant = executiveParticipant.find_next_sibling('p')
                            speech = executiveParticipant.getText()
                            executiveParticipant = executiveParticipant.find_next_sibling('p')

                            while executiveParticipant is not None and executiveParticipant.getText().replace(" ","") != search_result.replace(" ","") \
                                and 'Question-and-Answer' not in executiveParticipant.getText() and 'Operator' not in executiveParticipant:
                                speech += ', ' + executiveParticipant.getText()
                                executiveParticipant = executiveParticipant.find_next_sibling('p')
                                if executiveParticipant is not None:
                                    search_result = re.search(r'\b' + executiveParticipant.getText() + '\W', executiveParticipants)
                                    if search_result is None:
                                        search_result = ""
                                    else:
                                        search_result = search_result.group()

                            
                            speech_line=[conference_id,conference_url, speechPerson, speech]

                            with open('rawData-speech.csv','a', newline='') as f:
                                try:
                                    writer=csv.writer(f)
                                    writer.writerow(speech_line)
                                except UnicodeEncodeError:
                                    num_uncoded +=1
                        else:
                            executiveParticipants += ', Operator'

            elif paragraph.string == 'Conference Call Participants':
                callParticipant = paragraph.find_next_sibling('p')
                callParticipants = callParticipant.getText()
                callParticipant = callParticipant.find_next_sibling('p')

                while 'Question-and-Answer' not in callParticipant.getText() and (time.time() < timeout_start + timeout):
                    
                    if callParticipant is not None:
                        search_result = re.search(r'\b' + callParticipant.getText() + '\W', callParticipants)
                        if search_result is None:
                            search_result = re.search(r'\b' + callParticipant.getText() + '\W', comapnyParticipants)
                            if search_result is None:
                                search_result = ""
                            else:
                                search_result = search_result.group()

                        if callParticipant.getText().replace(" ","") != search_result.replace(" ","") and \
                            callParticipant.getText() != 'Operator':

                            callParticipants += ', ' + callParticipant.getText()
                            callParticipant = callParticipant.find_next_sibling('p')

                        elif callParticipant.getText().replace(" ","") == search_result.replace(" ","")  or \
                            callParticipant.getText() == 'Operator':
                            # print(callParticipant)
                            speechPerson = callParticipant.getText()
                            speech = ""
                            callParticipant = callParticipant.find_next_sibling('p')
                            speech = callParticipant.getText()
                            callParticipant = callParticipant.find_next_sibling('p')

                            while callParticipant is not None and callParticipant.getText().replace(" ","") != search_result.replace(" ","") \
                                and 'Question-and-Answer' not in callParticipant.getText() and 'Operator' not in callParticipant:
                                speech += ', ' + callParticipant.getText()
                                callParticipant = callParticipant.find_next_sibling('p')
                                if callParticipant is not None:
                                    search_result = re.search(r'\b' + callParticipant.getText() + '\W', callParticipants)
                                    if search_result is None:
                                        search_result = re.search(r'\b' + callParticipant.getText() + '\W', comapnyParticipants)
                                        if search_result is None:
                                            search_result = ""
                                        else:
                                            search_result = search_result.group()

                            
                            speech_line=[conference_id,conference_url, speechPerson, speech]

                            with open('rawData-speech.csv','a', newline='') as f:
                                try:
                                    writer=csv.writer(f)
                                    writer.writerow(speech_line)
                                except UnicodeEncodeError:
                                    num_uncoded +=1
                        else:
                            callParticipants += ', Operator'


            elif paragraph.getText() == 'Operator':
                if paragraph.find_next_sibling('p') is not None:
                    operator = paragraph.find_next_sibling('p').getText()
                    

            if 'Operator' in comapnyParticipants:
                comapnyParticipants = comapnyParticipants.replace(', Operator','')
            elif 'Operator' in corporateParticipants:
                corporateParticipants = corporateParticipants.replace(', Operator','')
            elif 'Operator' in executiveParticipants:
                executiveParticipants = executiveParticipants.replace(', Operator','')
            elif 'Operator' in callParticipants:
                callParticipants = callParticipants.replace(', Operator','')
            elif 'Conference Call Participants' in comapnyParticipants:
                comapnyParticipants = comapnyParticipants.replace(', Conference Call Participants','')
            elif 'Conference Call Participants' in corporateParticipants:
                corporateParticipants = corporateParticipants.replace(', Conference Call Participants','')
            elif 'Conference Call Participants' in executiveParticipants:
                executiveParticipants = executiveParticipants.replace(', Conference Call Participants','')
            elif 'None' in callParticipants:
                callParticipants = callParticipants.replace(', None','')
    
        print(conference_url, comapnyParticipants)

        participant_line=[conference_id,conference_url,comapnyParticipants, corporateParticipants, executiveParticipants, \
            callParticipants, operator, QA]
        

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

