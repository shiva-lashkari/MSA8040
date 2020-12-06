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
# with open("index.html") as page:
#     soup = BeautifualSoup(page)
url = "https://seekingalpha.com/earnings/earnings-call-transcripts"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
page = requests.get(url, headers = headers)
# soup = BeautifulSoup(page.text, 'html.parser')
soup = BeautifulSoup(page.text, 'html5lib')
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
            author = desc.find('a', recursive = False).text
        except:
            desc = 'None'
            author = 'None'
        try:
            symbol = post.find('span', class_='article-symbols')
            groupTitleTag = symbol.find('a')
            groupTitle = groupTitleTag['title']
            group = groupTitleTag.text
        except:
            groupTitleTag = 'None'
            groupTitle = 'None'
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

        post_line=[title,group,groupTitle,date,author,postUrl]

        with open('rawData.csv','a') as f:
                try:
                    writer=csv.writer(f)
                    writer.writerow(post_line)
                except UnicodeEncodeError:
                    num_uncoded +=1
    counter += 1

    next_page = 'https://seekingalpha.com/earnings/earnings-call-transcripts/' + str(counter)
    time.sleep(2)
    page = requests.get(next_page, headers = headers)
    soup = BeautifulSoup(page.text, 'html5lib')
    posts = soup.find_all('li', attrs = attrs)