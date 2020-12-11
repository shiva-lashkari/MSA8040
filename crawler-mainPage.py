from bs4 import BeautifulSoup
import requests
import os
import re
import time
import csv
import random
import requests
# from selenium import webdriver
from datetime import date, timedelta, datetime
import json
import MySQLdb

def readMain(url):
    url = url
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    # soup = BeautifulSoup(page.text, 'html5lib')
    attrs = {'class': 'list-group-item article'}
    posts = soup.find_all('li', attrs = attrs)

    counter = 1
    while (counter <= 1300):

        for post in posts:
            head = post.find('h3')
            title = head.find('a', class_='dashboard-article-link').text
            try:
                postUrl = 'https://seekingalpha.com' + head.find('a').attrs['href']
            except:
                postUrl = 'None'
            try:
                desc = post.find('div', class_ = 'article-desc')
                postDesc = desc.find('a', recursive = False).text
            except:
                desc = 'None'
                postDesc = 'None'
            try:
                symbol = post.find('span', class_='article-symbols')
                coTitleTag = symbol.find('a')
                coTitle = coTitleTag['title']
                group = coTitleTag.text
            except:
                coTitleTag = 'None'
                coTitle = 'None'
                group = 'None'
            try:
                # bullet = post.find('span', class_='bullet')
                dateTemp = post.find('span', class_='bullet').find_next_sibling(string = True)
                dateTemp = re.sub(r',|\.| +|\n', ' ', dateTemp).lstrip()
                dateTemp = re.sub(' PM','PM',dateTemp).rstrip()
                dateTemp = re.sub(' AM','AM',dateTemp)
                try:
                    date = datetime.strptime(str(datetime.now().year) + ' ' + dateTemp, '%Y %a %b %d %I:%M%p')
                except:
                    date = datetime.strptime(dateTemp, '%b %d %Y %I:%M%p')
                # date = re.match(r'(\S)$',date)
            except:
                date = 'None'


            cur = db.cursor()
            sql = 'INSERT INTO rawMainData (conference_Title, conference_date, company_ticker, company_name, \
                                        conference_type,conference_url) VALUES (%s, %s, %s, %s, %s, %s)'
            val = ((title,date, group,coTitle,postDesc,postUrl))
            cur.execute(sql,val)
            db.commit();
            
            # post_line=[title,date, group,coTitle,postDesc,postUrl]
            
            # with open('rawData.csv','a') as f:
            #         try:
            #             writer=csv.writer(f)
            #             writer.writerow(post_line)
            #         except UnicodeEncodeError:
            #             num_uncoded +=1
        counter += 1

        next_page = 'https://seekingalpha.com/earnings/earnings-call-transcripts/' + str(counter)
        time.sleep(2)
        page = requests.get(next_page, headers = headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        posts = soup.find_all('li', attrs = attrs)

with open('/home/shiva/myCodes/finalDM/MSA8040/config.json') as json_data_file:
    config = json.load(json_data_file)
    db = MySQLdb.connect(host=config['mysql']['host'],
                          user=config['mysql']['user'],
                          passwd=config['mysql']['passwd'],
                          db=config['mysql']['db'])

readMain("https://seekingalpha.com/earnings/earnings-call-transcripts")

