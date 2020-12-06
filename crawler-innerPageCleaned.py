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

#This function read each paragraph and seperate Title/Participents and speeches
def readType(conference_id, conference_url, paragraph,comapnyParticipants, corporateParticipants):
    catParticipents = []
    catParticipentTag = paragraph.find_next_sibling('p')
    catParticipents = catParticipentTag.getText()
    catParticipentTag = catParticipentTag.find_next_sibling('p')
    with open('rawData-speech.csv','a', newline='') as f:
        while catParticipentTag is not None and 'Conference Call Participants' not in catParticipents and \
            'Corporate Participants' not in catParticipents and 'Executives' not in catParticipents and \
            'Question-and-Answer' not in catParticipentTag.getText() and (time.time() < timeout_start + timeout):

            if catParticipentTag is not None:
                search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', catParticipents)
                if search_result is None:
                    if(comapnyParticipants != []):
                        search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', comapnyParticipants)
                    if(corporateParticipants != []):
                        search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', corporateParticipants)
                    if search_result is None:
                        search_result = ""
                    else:
                        search_result = search_result.group()
                        search_result = search_result.replace(" ","")
                        search_result = search_result.replace(",","")
                else:
                    search_result = search_result.group()
                    search_result = search_result.replace(" ","")
                    search_result = search_result.replace(",","")


                if catParticipentTag.getText().replace(" ","") != search_result and \
                    catParticipentTag.getText() != 'Operator':
                    
                    catParticipents += ', ' + catParticipentTag.getText()
                    catParticipentTag = catParticipentTag.find_next_sibling('p')
                    
                    
                elif catParticipentTag is not None and (catParticipentTag.getText().replace(" ","") == search_result or \
                    catParticipentTag.getText() == 'Operator' or catParticipentTag.getText() == 'Presentation'):

                    speechPerson = catParticipentTag.getText()
                    speech = ""
                    catParticipentTag = catParticipentTag.find_next_sibling('p')
                    speech = catParticipentTag.getText()
                    catParticipentTag = catParticipentTag.find_next_sibling('p')

                    while catParticipentTag is not None and catParticipentTag.getText().replace(" ","") != search_result \
                        and 'Question-and-Answer' not in catParticipentTag.getText() and 'Operator' not in catParticipentTag:
                        speech += ', ' + catParticipentTag.getText()
                        catParticipentTag = catParticipentTag.find_next_sibling('p')
                        if catParticipentTag is not None:
                            search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', catParticipents)
                            if search_result is None:
                                if(comapnyParticipants != []):
                                    search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', comapnyParticipants)
                                if(corporateParticipants != []):
                                    search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', corporateParticipants)
                                if search_result is None:
                                    search_result = ""
                                else:
                                    search_result = search_result.group()
                                    search_result = search_result.replace(" ","")
                                    search_result = search_result.replace(",","")
                            else:
                                search_result = search_result.group()
                                search_result = search_result.replace(" ","")
                                search_result = search_result.replace(",","")
                        # print(catParticipentTag.getText())
                        # print('$$$$$$$')
                        # print(search_result)

                    
                    speech_line=[conference_id,conference_url, speechPerson, speech]
                    
                    # print(speech_line)
                    
                    try:
                        writer=csv.writer(f)
                        writer.writerow(speech_line)
                    except UnicodeEncodeError:
                        num_uncoded +=1
            else:
                catParticipents += ', Operator'
    return catParticipents

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
        Presentation = 0
        for paragraph in innerPostparagraphs:
            #Change QA boolean to True if page contain 'Question-and-Answer Session'
            if 'Question-and-Answer Session' in paragraph.getText():
                QA = 1
            if 'Presentation' in paragraph.getText():
                Presentation = 1
            #Run the readType base on the tile 
            # Then we can seperate Company participents and Corporate participenta ans Call participetns and Executives
            if paragraph.getText() == 'Company Participants':
                comapnyParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)
                
            elif paragraph.getText() == 'Corporate Participants':
                corporateParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)

            elif paragraph.string == 'Executives':
                executiveParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)

            elif paragraph.string == 'Conference Call Participants':
                callParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)

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
            callParticipants, operator, QA, Presentation]
        

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
            break

