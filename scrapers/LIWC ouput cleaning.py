# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 14:41:42 2015

@author: Talha
"""

import pandas as pd

pn = pd.read_csv('data/LIWC2015 Results (ln).csv')
pn = pn.rename(columns={'Source (A)':'dt','Source (B)':'outlet','Source (C)':'story'})
pn = pn.drop([0,1])
#pn.to_csv('data/published.csv',index=False)
published = pn.drop('story',axis=1)
#published.to_csv('data/published-no-story.csv',index=False)

tn = pd.read_csv('data/LIWC2015 (all-tw).csv',encoding='utf-8')
tn = tn.drop(0)
tw = pd.read_csv('data/tw-sp.csv')
merged = tw.merge(tn,on='href')
merged = merged.drop_duplicates()
merged = merged.drop(['dt_y','fname'],axis=1)
merged = merged.rename(columns={'dt_x':'dt','sp':'tb'})
merged.to_csv('data/tweeted.csv',index=False)
tweeted = merged.drop('newstxt',axis=1)
tweeted.to_csv('data/tweeted-no-story.csv',index=False,encoding='utf-8')






# Read the datasets
outlets = "ABC NBCNews CBSNews FoxNews AP WPOST NYT CNN".split()
dfs = [pd.read_csv('data/tweets/'+outlet+'.csv') for outlet in outlets]
df = pd.DataFrame(columns=dfs[0].columns)
for i,df2 in enumerate(dfs):
    df2['outlet'] = outlets[i]
    df = df.append(df2)

df['fname'] = df.url.str.replace('^.*/','')
df.to_csv('data/tweets/all_tweets.csv',index=False,encoding='utf-8')

lw = pd.read_csv('data/tweets/all_tweets.csv') #25K
tn = pd.read_csv('data/LIWC2015 (all-tw).csv',encoding='utf-8') #23K
tn = tn.drop(0)
lw = lw.drop_duplicates('fname') #22K
tn = tn.drop_duplicates('fname') #19K
merged = lw.merge(tn,on='fname') #12568

merged.to_csv('data/tw-liwc.csv',index=False,encoding='utf-8')
nonews = merged.drop('newstxt',axis=1)
nonews.to_csv('data/tw-liwc-nonews.csv',index=False,encoding='utf-8')




cnn = pd.read_csv('data/LIWC2015 Results (cnn-joined).csv')
nyt = pd.read_csv('data/LIWC2015 Results (nyt-joined).csv')
cnn = cnn.drop(0)
nyt = nyt.drop(0)
tw = pd.read_csv('data/tw-liwc.csv')
tw = tw.drop(['fname','src','twid'],axis=1)
to_replace = ['Source (A)', 'Source (B)', 'Source (C)', 'Source (D)', 'Source (E)', 'Source (F)', 'Source (G)', 'Source (H)', 'Source (I)', 'Source (J)', 'Source (K)']
replace_with = ['tweep', 'twtext', 'fav', 'rt', 'url', 'href', 'dt', 'title', 'newstxt', 'cat', 'polarity']
r = dict(zip(to_replace,replace_with))
nyt['outlet'] = 'NYT'
cnn['outlet'] = 'CNN'
cn = cnn.append(nyt)
cn = cn.rename(columns=r)
cn = cn.drop(['cat','polarity'],axis=1)
a = tw.append(cn)
a.to_csv('data/tw-liwc.csv',index=False,encoding='utf-8')
nonews = a.drop('newstxt',axis=1)
nonews.to_csv('data/tw-liwc-nonews.csv',index=False,encoding='utf-8')




#import requests
#urls = df.url.unique()
#           
#def x(url):
#    try:
#        u = requests.head(url, allow_redirects=True).url
#        return {url:u}
#    except:
#        return {url:''}
#res = {}
#for i,u in enumerate(urls):
#    res.update(x(u))
#    if i%100==0:
#        print(i)





import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['savefig.dpi'] = 150
plt.style.use('ggplot')

import seaborn as sns
sns.set(color_codes=True)
sns.set_palette(sns.color_palette("husl", 8));
#read the data -> pn: published news, tn: tweeted news
pn = pd.read_csv('data/published-no-story.csv',encoding='utf-8')
tn = pd.read_csv('data/tw-liwc-nonews.csv',encoding='utf-8')

outlets = sorted(pn['outlet'].unique().tolist())
pn['sp'] = pn['posemo']-pn['negemo']
tn['sp'] = tn['posemo']-tn['negemo']

splim=(-.32, .42)
sns.mpl.rc("figure", figsize=(10,4))
sns.kdeplot(pn['sp'],label='Published News')
sns.kdeplot(tn['sp'],label='Tweeted News')
ax = sns.kdeplot(tn['sp'],tn.rt,label='Retweeted News')
ax.set_title('Comparing Sentiment Polarity of News Published/Tweeted/Retweeted - All Outlets Combined')
ax.set_xlabel('Sentiment Polarity')
ax.set_ylabel('Density')

