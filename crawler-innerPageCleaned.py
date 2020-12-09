import os
from bs4 import BeautifulSoup
import requests
import random
import re
import csv
import time
from datetime import date, timedelta, datetime
from selenium import webdriver


browser = webdriver.Chrome(executable_path = '/home/shiva/myCodes/finalDM/chromedriver')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

counter = 1
timeout = 20
failedURLs = []

#This function compare paragraph text with the name of the participents to find their speech
def searchResult(catParticipentTag, catParticipents):
    search_result = ""
    if catParticipentTag is not None:
        try:
            search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', catParticipents)
        except:
            search_result = ""
        if search_result is None or search_result == "":
            if(comapnyParticipants != []):
                try:
                    search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', comapnyParticipants)
                except:
                    search_result = ""
            if(corporateParticipants != []):
                try:
                    search_result = re.search(r'\b' + catParticipentTag.getText() + '\W', corporateParticipants)
                except:
                    search_result = ""
            if search_result is None or search_result == "":
                search_result = ""
            else:
                search_result = search_result.group()
                search_result = search_result.replace(" ","")
                search_result = search_result.replace(",","")
        else:
            search_result = search_result.group()
            search_result = search_result.replace(" ","")
            search_result = search_result.replace(",","")
    return(search_result)


#This function read each paragraph : 1- Find the participents base on the argomans and seperate them
#Also, find the speech for each person
def readType(conference_id, conference_url, paragraph,comapnyParticipants, corporateParticipants):
    catParticipents = []
    catParticipentTag = paragraph.find_next_sibling('p')
    if catParticipentTag.getText() != 'Operator':
        catParticipents = catParticipentTag.getText()
        catParticipentTag = catParticipentTag.find_next_sibling('p')

    with open('rawData-speechTest.csv','a', newline='') as f:
        while catParticipentTag is not None and 'Conference Call Participants' not in catParticipents and \
            'Corporate Participants' not in catParticipents and 'Executives' not in catParticipents and \
            'Question-and-Answer' not in catParticipentTag.getText() and (time.time() < timeout_start + timeout):

            #We are Checking the content of the paragraph with the participents name
            search_result = searchResult(catParticipentTag,catParticipents)

            #if paragraph text not equal to participents name/operator, it means this paragraph is participent and we add it to participent list
            if catParticipentTag.getText().replace(" ","") != search_result and \
                catParticipentTag.getText() != 'Operator':
                catParticipents += ' / ' + catParticipentTag.getText()
                catParticipentTag = catParticipentTag.find_next_sibling('p')
            
            #if paragraph text be equal to participents name/operator, it means next paragraph is contain the speech of this paragraphs participent
            #  and we add it to speechs
            elif catParticipentTag is not None and (catParticipentTag.getText().replace(" ","") == search_result or \
                catParticipentTag.getText() == 'Operator' or catParticipentTag.getText() == 'Presentation'):
                
                speechPerson = catParticipentTag.getText()
                speech = ""
                catParticipentTag = catParticipentTag.find_next_sibling('p')
                speech = catParticipentTag.getText()
                catParticipentTag = catParticipentTag.find_next_sibling('p')

                # We stop it if the paragraph be equal to Question-and-Answer or Operator because in most of the cases the operator has speech at the end of the 
                # conferance, we caugh this speech in line #161 then we can stop it in this point
                while catParticipentTag is not None and catParticipentTag.getText().replace(" ","") != search_result \
                    and 'Question-and-Answer' not in catParticipentTag.getText() and 'Operator' not in catParticipentTag:

                    if catParticipentTag.getText().replace(" ","") != searchResult(catParticipentTag,catParticipents):
                        speech += ', ' + catParticipentTag.getText()
                        catParticipentTag = catParticipentTag.find_next_sibling('p')
                        search_result = searchResult(catParticipentTag,catParticipents)
                    else:
                        search_result = searchResult(catParticipentTag,catParticipents)
                
                speech_line=[conference_id,conference_url, speechPerson, speech]
                
                try:
                    writer=csv.writer(f)
                    writer.writerow(speech_line)
                except UnicodeEncodeError:
                    num_uncoded +=1
        else:
            catParticipents += ' / ' + 'Operator'
    #We need to delete the title paragraphs from our participents list
    if 'Operator' in catParticipents:
        catParticipents = catParticipents.replace(' / Operator','')
    if 'Operator' in catParticipents:
        catParticipents = catParticipents.replace('Operator','')
    elif 'Conference Call Participants' in catParticipents:
        catParticipents = catParticipents.replace(' / Conference Call Participants','')

    return catParticipents

with open('rawData-test.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        timeout_start = time.time()
        participants = []
        # conference_url = ("https://seekingalpha.com/article/4392903-idt-corporations-idt-ceo-shmuel-jonas-on-q1-2021-results-earnings-call-transcript")
        conference_url = (row[-1])
        conference_id = (row[0])
        browser.get(conference_url)
        html = browser.page_source
        # innerSoup = BeautifulSoup(html, "lxml")
        innerSoup = BeautifulSoup(html, 'html.parser')
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
            # if 'Presentation' in paragraph.getText():
            #     Presentation = 1
            # Run the readType base on the title 
            # Then we can seperate Company participents and Corporate participenta ans Call participetns and Executives
            if paragraph.getText() == 'Company Participants' or paragraph.getText() == 'Company Participants ':
                comapnyParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)
                
            elif paragraph.getText() == 'Corporate Participants':
                corporateParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)

            elif paragraph.string == 'Executives':
                executiveParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)

            elif paragraph.string == 'Conference Call Participants':
                callParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants)
                if paragraph.find_next_sibling('p').getText() == 'Operator':
                    callParticipants = []

            elif paragraph.getText() == 'Operator':
                if paragraph.find_next_sibling('p') is not None:
                    operator = paragraph.find_next_sibling('p').getText()
                    
    
        print(conference_url, comapnyParticipants)

        participant_line=[conference_id,conference_url,comapnyParticipants, corporateParticipants, executiveParticipants, \
            callParticipants, operator, QA, Presentation]
        

        with open('rawData-result-Test.csv','a', newline='') as f:
            try:
                writer=csv.writer(f)
                writer.writerow(participant_line)
            except UnicodeEncodeError:
                num_uncoded +=1
        time.sleep(2)
        
        #if captcha stop the crawler it returns null for comapnyParticipants and corporateParticipants
        #we stop the code if it happens more than 5 times
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
        # break
