import os
from bs4 import BeautifulSoup
import requests
import random
import re
import csv
import time
from datetime import date, timedelta, datetime
from selenium import webdriver
import json
import MySQLdb

browser = webdriver.Chrome(executable_path = '/home/shiva/myCodes/finalDM/chromedriver')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


timeout = 50


#This function compare paragraph text with the name of the participents to find their speech
def searchResult(catParticipentTag, catParticipents, comapnyParticipants, corporateParticipants):
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
def readType(conference_id, conference_url, paragraph,comapnyParticipants, corporateParticipants, timeout_start):
    catParticipents = []
    catParticipentTag = paragraph.find_next_sibling('p')
    if catParticipentTag.getText() != 'Operator':
        catParticipents = catParticipentTag.getText()
        catParticipentTag = catParticipentTag.find_next_sibling('p')

    # with open('rawData-speechTest.csv','a', newline='') as f:
    while catParticipentTag is not None and 'Conference Call Participants' not in catParticipents and \
        'Corporate Participants' not in catParticipents and 'Executives' not in catParticipents and \
        'Question-and-Answer' not in catParticipentTag.getText() and (time.time() < timeout_start + timeout):

        #We are Checking the content of the paragraph with the participents name
        search_result = searchResult(catParticipentTag, catParticipents, comapnyParticipants, corporateParticipants)

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

                if catParticipentTag.getText().replace(" ","") != searchResult(catParticipentTag, catParticipents, comapnyParticipants, corporateParticipants):
                    speech += ', ' + catParticipentTag.getText()
                    catParticipentTag = catParticipentTag.find_next_sibling('p')
                    search_result = searchResult(catParticipentTag, catParticipents, comapnyParticipants, corporateParticipants)
                else:
                    search_result = searchResult(catParticipentTag, catParticipents, comapnyParticipants, corporateParticipants)
            
            # speech_line=[conference_id,conference_url, speechPerson, speech]
            
            # try:
            #     writer=csv.writer(f)
            #     writer.writerow(speech_line)
            # except UnicodeEncodeError:
            #     num_uncoded +=1

            
            cur = db.cursor()
            sql = 'INSERT INTO rawSpeechData (conference_id, conference_url, pa_name, textual_info) VALUES (%s, %s, %s, %s)'
            val = ((conference_id, conference_url, speechPerson, speech))
            cur.execute(sql,val)
            db.commit();
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

# with open('rawData-test.csv', 'r') as file:
def readMain():
    counter = 1
    failedURLs = []
    # reader = csv.reader(file)
    cur = db.cursor()
    cur.execute("TRUNCATE TABLE `rawInnerData`")
    cur.execute("TRUNCATE TABLE `rawSpeechData`")
    db.commit();

    #dataTest is the sample table that I bult with those 10 urls provided for presentation
    conferenceList = cur.execute('Select * FROM `rawMainData`')
    conferenceList = cur.fetchall()
    for row in conferenceList:
        timeout_start = time.time()
        participants = []
        conference_url = (row[-1])
        conference_id = (row[0])
        browser.get(conference_url)
        html = browser.page_source
        # innerSoup = BeautifulSoup(html, "lxml")
        innerSoup = BeautifulSoup(html, 'html.parser')
        innerPostparagraphs = innerSoup.find_all('p')
        
        time.sleep(2)
        comapnyParticipants = ""
        corporateParticipants = ""
        executiveParticipants = ""
        callParticipants = ""
        speech = ""
        operator = ""
        for paragraph in innerPostparagraphs:
            # Run the readType base on the title 
            # Then we can seperate Company participents and Corporate participenta ans Call participetns and Executives
            if paragraph.getText() == 'Company Participants' or paragraph.getText() == 'Company Participants ':
                comapnyParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants, timeout_start)
                
            elif paragraph.getText() == 'Corporate Participants':
                corporateParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants, timeout_start)

            elif paragraph.string == 'Executives':
                executiveParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants, timeout_start)

            elif paragraph.string == 'Conference Call Participants':
                callParticipants = readType(conference_id,conference_url, paragraph, comapnyParticipants , corporateParticipants, timeout_start)
                if paragraph.find_next_sibling('p').getText() == 'Operator':
                    callParticipants = []

            elif paragraph.getText() == 'Operator':
                if paragraph.find_next_sibling('p') is not None:
                    operator = paragraph.find_next_sibling('p').getText()
                    
    
        print(conference_url, comapnyParticipants)
#Writing code to csv

        # participant_line=[conference_id,conference_url,comapnyParticipants, corporateParticipants, executiveParticipants, \
        #     callParticipants, operator]
        

        # with open('rawData-result-Test.csv','a', newline='') as f:
        #     try:
        #         writer=csv.writer(f)
        #         writer.writerow(participant_line)
        #     except UnicodeEncodeError:
        #         num_uncoded +=1

        time.sleep(2)
        sql = 'INSERT INTO rawInnerData (conference_id, conference_url, companyParticipants, corporateParticipants, \
                                    executiveParticipants,callParticipants, operator) VALUES (%s, %s, %s, %s, %s, %s, %s)'

        val = ((conference_id,conference_url, str(comapnyParticipants), str(corporateParticipants), str(executiveParticipants), str(callParticipants), str(operator)))
        cur.execute(sql,val)
        db.commit();
        
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

# The path of json file
with open('/home/shiva/myCodes/finalDM/MSA8040/config.json') as json_data_file:
    config = json.load(json_data_file)
    db = MySQLdb.connect(host=config['mysql']['host'],
                          user=config['mysql']['user'],
                          passwd=config['mysql']['passwd'],
                          db=config['mysql']['db'])

readMain()

Select 
case when pa_organization="NULL" then count(participant_id) end as 'company_participants',
case when pa_organization!="NULL" then count(participant_id)  end as 'conference_call_participant'
FROM (select participant_id, pa_organization
from  company co inner join conference cc using(company_id)
inner join speech using(conference_id)
inner join  participant using(participant_id)
where company_ticker = 'MNR' and conference_date = '2020-11-24') As myTable