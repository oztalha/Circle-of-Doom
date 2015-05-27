# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:15:54 2015

First get these from tweets:
twid, tweep, twtext, fav, rt, url
Then will add these:
dt, title, content

@author: Talha
"""

import json
import pandas as pd
import glob
import os
import urllib

path="data/tweets/"
filenames = glob.glob(path+'*.json')
for filename in filenames:
    with open(filename, encoding='utf-8') as f:
        tweep = json.load(f)
        df = pd.DataFrame(columns=['twid', 'tweep', 'twtext', 'fav', 'rt', 'url'])
        for i,status in enumerate(tweep['data']):
            df.loc[i,'twid'] = status['id']
            try:
                df.loc[i,'fav'] = status['retweeted_status']['favorite_count']
                df.loc[i,'rt'] = status['retweeted_status']['retweet_count']
                df.loc[i,'twtext'] = status['retweeted_status']['text']
                for twp in status['entities']['user_mentions']:
                    if (status['retweeted_status']['user']['id_str'] == twp['id_str']):
                        df.loc[i,'tweep'] = twp['screen_name']
                        break
                try:
                    df.loc[i,'url'] = ' '.join([url['expanded_url'] for url in status['retweeted_status']['entities']['urls']])
                except:
                    df.loc[i,'url'] = ''
            except:
                df.loc[i,'tweep'] = tweep['parameters']['screen_name']
                df.loc[i,'twtext'] = status['text']
                df.loc[i,'fav'] = status['favorite_count']
                df.loc[i,'rt'] = status['retweet_count']
                try:
                    df.loc[i,'url'] = ' '.join([url['expanded_url'] for url in status['entities']['urls']])
                except:
                    df.loc[i,'url'] = ''
        df.to_csv(path+tweep['parameters']['screen_name']+'.csv',encoding='utf-8',index=False)
#df.to_csv("data/NYT-tweets.csv",encoding='utf-8',index=False)


def url_download():
    """
    apne,
    download.sh (single liner): wget -O $2 $1
    
    while read -r url; do
        ./download.sh $url
    done < list_of_urls
    """    
    import pandas as pd
    import glob
    import os
    #import urllib
    import requests
    path="data/tweets/"
    filenames = glob.glob(path+'*.csv')
    articles = {'abc':'abcn.ws', 'ap':'apne','washingtonpost':'wapo.st|washingtonpost',
                'bbcworld':'bbc','huffingtonpost':'huff','foxnews':'fxn.ws|foxnews',
                'time':'ti.?me'}
    for filename in filenames:
        outlet = filename.split('\\')[1].split('.')[0]
        df = pd.read_csv(filename,na_filter=False)
        single = df[~df.url.str.contains('[\s]')].url
        multip = df[df.url.str.contains('[\s]')].url
        multi0 = multip.apply(lambda x: x.split()[0])
        multi1 = multip.apply(lambda x: x.split()[1])
        ul = []
        for df in single,multi0,multi1:
            df = df[df.str.contains(articles[outlet])]
            ul.extend(df)
        print(outlet,len(ul))

        #start downloading process
        directory = 'htmls/'+outlet+'/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for i,url in enumerate(ul):
            fname = url.split('/')[-1]
            if os.path.exists(directory+fname):
                continue
            print(i,directory+fname)
            try:
                resource = requests.get(url,timeout=5) #urllib.request.urlopen(url,timeout=5)
                # content = resource.read().decode(resource.headers.get_content_charset())
                # encoding = resource.headers.get_content_charset()                
                with open(directory+fname,'w',encoding=resource.encoding) as w: 
                    w.write(resource.text) #content
            except Exception as e:
                print(e)
                print(url)
        # pd.Series(ul).to_csv(filename.split('.')[0]+'txt',index=False)
    

def nyt_url_list():
    df = pd.read_csv('data/NYT-tweets.csv',na_filter=False)
    multip = df[df.url.str.contains(' ')].url
    multip
    multi = multip.apply(lambda x: x.split()[1])
    #ul.extend([j for i in l for j in i]) #flatten and extend
    single = df[~df.url.str.contains('[\s]')].url
    single = single[single.str.contains('http')]
    ul = []
    ul.extend(multi.tolist())
    ul.extend(single.tolist())
    #3 bitly URLs <- df[~df.url.str.contains('nyt')].url
    pd.Series(ul).to_csv('data/urls_nyt.csv',index=False)

def cnn_url_list():
    df = pd.read_csv('data/cnn.csv',na_filter=False)
    multip = df[df.url.str.contains(' ')].url
    multip
    multi = multip.apply(lambda x: x.split())
    single = df[~df.url.str.contains('[\s]')].url
    single = single[single.str.contains('http')]
    ul = []
    ul.extend([j for i in multi.tolist() for j in i]) #flatten and extend
    ul.extend(single.tolist())
    ul = [url for url in ul if 'cnn' in url or 'CNN' in url]
    pd.Series(ul).to_csv('data/urls_cnn.csv',index=False)

