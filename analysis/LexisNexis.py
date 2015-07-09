# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 09:37:12 2015

@author: Talha
"""

import pandas as pd
import numpy as np
import textblob as tb
import os
import time

outlets = "AP ABC NBCNews WPOST CBSNews FoxNews CNN".split()
df = pd.DataFrame(columns=['outlet','dt','sp'])
dailies = []
for outlet in outlets:
    path = 'Lexis Doom/'+outlet+' Lexis/'
    day = {}
    for daily in os.listdir(path):
        try:
            with open(path+daily, 'r',encoding='utf-8') as f:
                news = f.read()
            dti = 7 if outlet == 'WPOST' else 6
            dt = pd.to_datetime(news[:200].split('\n')[dti].strip()).date()
            if 'dt' in day and dt == day['dt']:
                day['news'] += news
            else:
                day['outlet'] = outlet
                day['dt'] = dt
                day['sp'] = tb.TextBlob(news).sentiment.polarity
                dailies.append(day)
                day = {}
        except Exception as e:
            print(path+daily)
            
            
df=pd.DataFrame(dailies)   
df.to_csv('data/ln-sp.csv',index=False)
