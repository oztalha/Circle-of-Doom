# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:04 2015

@author: Talha
"""

import pandas as pd
from bs4 import BeautifulSoup
import os

"""
import urllib
from http import cookiejar
cj= cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
url = 'http://www.nytimes.com/2015/02/23/sports/bol-bol-6-foot-10-son-of-manute-adjusts-to-high-school-basketball.html'
url = 'http://www.cnn.com/2015/01/20/politics/who-is-joni-ernst/index.html'
url='http://money.cnn.com/2015/01/21/news/economy/harold-hamm-divorce/index.html'
request = urllib.request.Request(url)
response = opener.open(request)
soup = BeautifulSoup(response, "lxml")
newstxt = '\n'.join([text.text for text in soup.findAll('p',{'itemprop':'articleBody'})])
print(newstxt)
"""

def get_NYT_news():
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    for i,html in enumerate(os.listdir('htmls/nyt/')):
        try:
            f = open('htmls/nyt/'+html,encoding='utf8')
            soup = BeautifulSoup(f, "lxml")
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'ptime'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            #newstxt = soup.find(id='story-body').text
            newstxt = '\n'.join([text.text for text in soup.findAll('p',{'class':"story-body-text story-content"})])
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (len(errors),dt, title, href)
            f.close()
        except:
            errors.append((i,html))

    #391 <- len(df[df.newstxt==''].href)
    df.to_csv("data/NYT-news.csv",encoding='utf-8',index=False)
    others = list(zip(*errors))[1]
    pd.Series(others).to_csv('data/other_urls_NYT.csv',index=False)
    return others
    

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
            #newstxt = soup.find('div',id='storytext').text
            newstxt = '\n'.join([text.text.strip() for text in soup.find('div',id='storytext').findAll(['p','h2'])])
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (len(errors),dt, title, href)
            f.close()
        except:
            errors.append((i,html))

    odds = list(zip(*errors))[1]
    #0 <- len(df[df.newstxt==''].href)
    df.to_csv("data/CNN-money.csv",encoding='utf-8',index=False)
    pd.Series(odds).to_csv('data/odd_urls_cnn.csv',index=False)
    return odds

    
def get_CNN_news():
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    for i,html in enumerate(os.listdir('htmls/cnn/')):
        try:
            f = open('htmls/cnn/'+html)
            soup = BeautifulSoup(f, "lxml")
            title = soup.title.text
            dt = pd.to_datetime(soup.find(class_="update-time").text[8:])
            href = soup.find(itemprop="url")['content']
            #newstxt = soup.find('section',id="body-text").text
            newstxt = '\n'.join([text.text for text in soup.findAll('p',{'class':'zn-body__paragraph'})])
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print (html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print (html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/CNN-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_cnn.csv',index=False)
    return others
    
    
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


"""
# 328 URLs could not be parsed:
# oddset = set([odd.split('%')[0] for odd in odds])
# 328 <- len(oddset)
df1 = pd.read_csv('data/CNN-news.csv',parse_dates=['dt'])
df1['cat']='news'
df2 = pd.read_csv('data/CNN-videos.csv',parse_dates=['dt'])
df2['cat']='video'
df3 = pd.read_csv('data/CNN-money.csv',parse_dates=['dt'])
df3['cat']='money'
df = pd.concat([df1,df2,df3])
df.to_csv("data/CNN-all.csv",encoding='utf-8',index=False)
"""