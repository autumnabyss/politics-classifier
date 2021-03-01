#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 00:32:49 2020

@author: yangdairu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from EmotionDec import Swinger
import tensorflow as tf
import json
#%% 
'''網頁擷取'''
# start_time = time.time()
def get_p(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml');
    paragh  = soup.find_all('p')
    paragh_list = []
    for p in paragh:
        if len(p.contents)>0 and p.contents[0] != "\n":
            word = ''
            for i in range (len(p.contents)):
                word += str(p.contents[i])
            paragh_list.append(word.strip())
    return paragh_list

url = 'https://tw.news.yahoo.com/%E7%B6%A0%E5%BC%B7%E5%B0%81%E6%AE%BA%E5%9C%A8%E9%87%8E%E6%8F%90%E6%A1%88-%E5%83%85%E6%A0%A1%E5%9C%92%E7%A6%81%E8%90%8A%E8%B1%AC%E4%BA%A4%E4%BB%98%E5%8D%94%E5%95%86-222010563.html'
p_list = get_p(url)
#%% 
'''Read Party Keyword'''
party_data = pd.read_csv('Party.csv')

def get_party(s, num, data):
    party = data[s]
    party = np.array(party[~pd.isnull(party)])
    party = np.concatenate([party.reshape(-1,1), np.ones((len(party), 1)).reshape(-1,1).astype('int')+num], axis = 1)
    return party

party_blue = get_party('藍', 0, party_data)
party_green = get_party('綠', 1, party_data)
party_red = get_party('紅', 2, party_data)
party_yellow = get_party('黃', 3, party_data)
party_white = get_party('白', 4, party_data)
party_kw = np.concatenate([party_blue, party_green, party_red, party_yellow, party_white], axis = 0)
#%%
'''Get Paragraph's Keyword-v2'''
def get_kw(p, kw):
    kw_count = {1: 0, 2:0, 3:0, 4:0, 5:0}
    for i in kw:
        cal_kw = p.count(i[0])
        if cal_kw > 0:
            # print(i[0])
            kw_count[i[1]] += cal_kw
    # print(kw_count)
    return kw_count    

def get_p_kw(p_list, party_kw):
    total_count = {1:0, 2:0, 3:0, 4:0, 5:0}
    total_kw = []
    for p in p_list:
        pty_cal = get_kw(p, party_kw)
        for i in total_count:
            total_count[i] += pty_cal[i]
        total_kw.append(pty_cal)
    total_kw = pd.DataFrame(total_kw).fillna(0)
    return total_kw

total_kw = get_p_kw(p_list, party_kw)
#%%
'''Emotion Analysis'''
s = Swinger()
s.load('LogisticRegression', useDefault=True) # 以LogisticRegression建立model
emotion_prob = []
for i in range(len(p_list)):
    prob = s.swing(p_list[i])
    emotion_prob.append(list(prob))
    # print(f"positive prob: {prob[0]}, negative prob: {prob[1]}")
#%%
total_kw = np.array(total_kw)
emotion_prob = np.array(emotion_prob)
pscore = []
for i in range (len(total_kw)):
    totals = np.sum(total_kw[i])
    if totals!=0:
        score = total_kw[i]*(emotion_prob[i][0]-emotion_prob[i][1])
        score = score / np.sum(abs(score))
        tmp = np.zeros(5)+50
        pscore.append(list(tmp+tmp*score))
final = list(pd.DataFrame(pscore).mean(axis=0).apply(lambda x: round(x,2) if True else x))
# print(time.time() - start_time)
#%%
'''傳入json檔給js'''
# with open('score.json', 'w') as f:
#     json.dump(final, f, ensure_ascii=False)
json_score = json.dumps(final, ensure_ascii=False)
print(json_score)
    
        
    





