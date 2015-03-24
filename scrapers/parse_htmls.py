# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:04 2015

@author: Talha
"""

import pandas as pd
from bs4 import BeautifulSoup
import os

# 328 URLs could not be parsed:
# oddset = set([odd.split('%')[0] for odd in odds])
# 328 <- len(oddset)

def get_CNN_money(remaining):
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    for i,html in enumerate(remaining):
        try:
            f = open('htmls/cnn/'+html)
            soup = BeautifulSoup(f, "lxml")
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'date'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            newstxt = soup.find('div',id='storytext').text
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (len(errors),dt, title, href)
            f.close()
        except:
            errors.append((i,html))

    odds = list(zip(*errors))[1]
    df.to_csv("data/CNN-money.csv",encoding='utf-8',index=False)
    pd.Series(odds).to_csv('data/odd_urls_cnn.csv',index=False)
    return odds

    
def get_CNN_news(others):
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    for i,html in enumerate(others):
        try:
            f = open('htmls/cnn/'+html)
            soup = BeautifulSoup(f, "lxml")
            title = soup.title.text
            dt = pd.to_datetime(soup.find(class_="update-time").text[8:])
            href = soup.find(itemprop="url")['content']
            newstxt = soup.find('section',id="body-text").text
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (len(errors),dt, title, href)
            f.close()
        except:
            errors.append((i,html))

    remaining = list(zip(*errors))[1]
    df.to_csv("data/CNN-news.csv",encoding='utf-8',index=False)
    pd.Series(remaining).to_csv('data/remaining_urls_cnn.csv',index=False)
    return remaining
    
    
def get_CNN_videos():
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    for i,html in enumerate(os.listdir('htmls/cnn/')):
        try:
            f = open('htmls/cnn/'+html)
            soup = BeautifulSoup(f, "lxml")
            title = soup.title.text
            #show = soup.find("span",class_='metadata--show__name').text.split(' ')[0]
            #source = soup.find(itemprop="sourceLink").text
            dt = pd.to_datetime(soup.find(class_="metadata__data-added").text[9:])
            href = soup.find(itemprop="url")['content']
            newstxt = soup.find('p',class_="media__video-description").text
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (len(errors),dt, title, href)
            f.close()
        except:
            errors.append((i,html))

    df.to_csv("data/CNN-videos.csv",encoding='utf-8',index=False)
    others = list(zip(*errors))[1]
    return others

