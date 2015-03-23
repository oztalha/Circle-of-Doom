# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
import pandas as pd
import re

df = pd.read_table('nytcnn.tsv',nrows=1,dtype={'id':str,'cnn':int,'nyt':int},parse_dates=['published_at'])
df = df[df.id==-1]
df['id']= df['id'].astype(str)
df['cnn']= df['cnn'].astype(int)
df['nytim']= df['nytim'].astype(int)

nyt = json.load(open('nyt.json', encoding='utf-8'))
cnn = json.load(open('cnn.json', encoding='utf-8'))
for j,tweep in enumerate((nyt,cnn)):
    for i,status in enumerate(tweep['data']):
        i = j*3200+i
        df.loc[i,'id'] = status['id']
        df.loc[i,'published_at'] = pd.datetools.parse(status['created_at'])
        df.loc[i,'lang'] = status['lang']
        df.loc[i,'text'] = status['text']
        df.loc[i,'cnn'] = 1 if re.search('\bcnn\b', status['text'], re.IGNORECASE) else 0
        df.loc[i,'nytim'] = 1 if re.search('\bnytimes\b', status['text'], re.IGNORECASE) else 0

df.to_csv("nytcnn.csv",date_format='%Y-%m-%d %H:%M:%S UTC',encoding='utf-8',index=False)