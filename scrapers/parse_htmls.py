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


def combine():
    """
    combine fi and tw using two methods:
    m1: inner join hrefs
    m2: inner join filename with url in tw
    """
    fi = pd.read_csv("data/nyt-filename-url.csv")
    tw = pd.read_csv('data/NYT-tweets.csv',na_filter=False)
    tw = tw.rename(columns={'url':'href'})
    m1 = fi.merge(tw, on='href', how='inner')
    #(48, 9) <- m1.shape
    
    tw2 = tw.copy()
    tw2['url'] = tw2.href.str.replace('^.*/','')
    m2 = fi.merge(tw2, left_on='filename', right_on='url', how='inner')
    #(2561, 11) <- m2.shape
    m2.to_csv('data/nyt-id-url.csv',columns=['twid','href_x'],header=['twid','href'],index=False)
    
    #m2.merge(m1,left_on='url',right_on='filename',how='inner').shape
    #(45, 20)

    fi = pd.read_csv("data/cnn-filename-url.csv")
    tw = pd.read_csv('data/cnn-tweets.csv',na_filter=False)
    tw = tw.rename(columns={'url':'href'})
    m1 = fi.merge(tw, on='href', how='inner')
    #(18, 9) <- m1.shape
    
    #method2 on single URLs and on first URL (in case of multiple urls)
    tw2 = tw.copy()
    tw2['url'] = tw2.href.str.replace('^.*/','')
    m2 = fi.merge(tw2, left_on='filename', right_on='url', how='inner')
    #(2651, 11) <- m2.shape
    
    #method2 on 2nd URL (in case of multiple URLs)
    multip = tw[tw.href.str.contains(' ')]
    multip['url'] = multip.apply(lambda x: pd.Series(x.href.split()[0]),axis=1)
    multip['url'] = multip['url'].str.replace('^.*/','')
    m22 = fi.merge(multip, left_on='filename', right_on='url', how='inner')
    #(268, 11) <- m22.shape
    m2 = m2.append(m22)
    m2.to_csv('data/cnn-id-url.csv',columns=['twid','href_x'],header=['twid','href'],index=False)
    #(2919, 11)<- m2.shape
    
    #multi = multip.apply(lambda x: x.append(pd.Series((x.href.split()[0],x.href.split()[1]))),axis=1)
    #multi = multi.rename(columns={0:'url1',1:'url2'})


def get_filename_url_tuples():
    
    errors = []
    df = pd.DataFrame(columns=('src','filename', 'href','title'))
    
    for src in ('nyt','cnn'):
        path='htmls/'+src+'/'
        for i,filename in enumerate(os.listdir(path)):
            try:
                f = open(path+filename,encoding='utf8')
                soup = BeautifulSoup(f, "lxml")
                title = soup.title.text
                href = soup.head.find('link',{'rel':'canonical'})['href']
                df.loc[len(df)+1]=[src, filename, href, title]
                print(src, filename, href, title)
            except:
                errors.append((src,filename))    
    
    pd.DataFrame(errors).to_csv('data/erroneous_html.csv',index=False, header=['src','filename'])
    df.to_csv("data/filename-url.csv",encoding='utf-8',index=False)
    
    nyt = df[df.src=='nyt']
    nyt['filename'] = nyt['filename'].str.replace('\.2$','')
    nyt['filename'] = nyt['filename'].str.replace('\.1$','')
    nyt['filename'] = nyt['filename'].str.replace('%0D$','')
    nyt.to_csv("data/nyt-filename-url.csv",encoding='utf-8',index=False)
    
    cnn = df[df.src=='cnn']
    cnn['filename'] = cnn['filename'].str.replace('\.2$','')
    cnn['filename'] = cnn['filename'].str.replace('\.1$','')
    cnn['filename'] = cnn['filename'].str.replace('%0D$','')
    cnn.to_csv("data/cnn-filename-url.csv",encoding='utf-8',index=False)



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


def get_ABC_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/abc/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'Date'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            texts = soup.findAll('p',{'itemprop':'articleBody'})
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/abc-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_abc.csv',index=False)
    return others
    
    
def get_AP_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/ap/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html)
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            #dateline > span:nth-child(1)
            dt = pd.to_datetime(soup.find(id='dateline').find('span').text)
            href = soup.head.find('link',{'rel':'canonical'})['href']
            #newstxt = soup.find('section',id="body-text").text

            texts = soup.find(class_='field field-name-body field-type-text-with-summary field-label-hidden entry-content').findAll('p')[1:]
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print (html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print (html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/AP-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_AP.csv',index=False)
    return others
    
    
    
def get_BBC_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/bbcworld/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
    
            dt = soup.find('p',{'class':'date date--v1'})
            if(dt):
                dt = pd.to_datetime(dt.find('strong').text)
                texts = soup.find(class_='map-body').findAll('p')
                newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            else:
                dt = soup.find('div',{'class':'date date--v2'}).text
                dt = pd.to_datetime(dt)
                texts = soup.find('div',{'property':'articleBody'}).findAll('p')
                newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/bbcworld-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_bbcworld.csv',index=False)
    
    
    
def get_FOX_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/foxnews/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            dt = pd.to_datetime(soup.head.find('meta',{'name':'dcterms.created'})['content'])
            href = soup.head.find('link',{'rel':'canonical'})['href']
            texts = soup.find('div',{'itemprop':'articleBody'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])
            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)
            
    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/foxnews-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_foxnews.csv',index=False)
    
    
    
def get_HUFF_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/huffingtonpost/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.head.find('meta',{'name':'sailthru.date'})['content'])        
            texts = soup.find('div',{'id':'mainentrycontent'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/huffingtonpost-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_huffingtonpost.csv',index=False)
    

def get_TIME_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/time/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.find('time',{'itemprop':'datePublished'})['datetime'])
            texts = soup.find('section',{'itemprop':'articleBody'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/time-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_time.csv',index=False)
    

def get_WP_news():
    df = pd.DataFrame(columns=('fname','dt', 'title', 'href', 'newstxt'))
    errors = []
    path = 'htmls/washingtonpost/'
    for i,html in enumerate(os.listdir(path)):
        try:
            f = open(path+html,encoding='utf-8')
            soup = BeautifulSoup(f, "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            title = soup.title.text
            href = soup.head.find('link',{'rel':'canonical'})['href']
            dt = pd.to_datetime(soup.find('span',{'class':'pb-timestamp'}).text)
            texts = soup.find('div',{'id':'article-body'}).findAll('p')
            newstxt = '\n\n'.join([text.text.strip() for text in texts if not text.text.isspace()])

            df.loc[len(df)+1]=[html, dt, title, href, newstxt]
            print ('[OK]:',html, dt, title, href)
            f.close()
        except:
            errors.append((i,html))
            print ('[ERROR]:',html, dt, title, href)

    others = list(zip(*errors))[1]
    #19 <- len(df[df.newstxt==''].href)
    df.to_csv("data/washingtonpost-news.csv",encoding='utf-8',index=False)
    pd.Series(others).to_csv('data/other_urls_washingtonpost.csv',index=False)