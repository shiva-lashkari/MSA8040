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
failedURLs = []
with open('rawData.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # timeout_start = time.time()
        participants = []
        # while(len(participants) == 0):
        conference_url = (row[-1])
        conference_id = (row[0])
        browser.get(conference_url)
        html = browser.page_source
        innerSoup = BeautifulSoup(html, "lxml")
        innerPostparagraphs = innerSoup.find_all('p')
        
        time.sleep(5)
        innerPageDetail = []
        for paragraph in innerPostparagraphs:
            while counter < 20:
                innerPageDetail += paragraph
                counter +=1
            
        
        print(conference_url,innerPageDetail)
        
                    
        participant_line=[conference_id,conference_url,innerPageDetail]
        

        with open('rawDataWhole.csv','a', newline='') as f:
            try:
                writer=csv.writer(f)
                writer.writerow(participant_line)
            except UnicodeEncodeError:
                num_uncoded +=1

        time.sleep(5)
