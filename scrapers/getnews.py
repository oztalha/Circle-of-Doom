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

tweep = json.load(open('data/cnn.json', encoding='utf-8'))
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
        
# 60 tweets have no URL for nytimes <- len(df[df.url==''])
# 605 tweets have no URL for cnn <- len(df[df.url==''])
# 6 tweets have 2+ URLs for nytime <- len(df[df.url.str.contains(' ')])
# 212 tweets have 2+ URLs for cnn <- len(df[df.url.str.contains(' ')])

df.to_csv("data/cnn.csv",encoding='utf-8',index=False)