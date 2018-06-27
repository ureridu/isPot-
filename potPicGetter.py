# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 20:08:49 2018

@author: Ureridu
"""

import pandas
import requester
import time
from concurrent.futures import ThreadPoolExecutor
from random import randint
import os


def get(inbit):
    name, url = inbit
    print(name)
    time.sleep(randint(3, 10))

#    print(url)
    resp = req(url)
    if resp:
        with open('images/' + name, 'wb') as outfile:
            outfile.write(resp.content)
    else:
        print('BADBADBADBAD')


data = pandas.read_excel('Pots.xlsx')
data.reset_index(inplace=True, drop=True)


req = requester.Requester()
bad = []
allList = []

for i, row in data.iterrows():
    pics = row['Pics'].replace('[', '').replace(']', '').replace("'", '').split(', ')
    pot, *_ = row['Text'].split(',')
    for pic in pics:
        *_, picName, _ = pic.split('/')
        picName = '%s__%s.jpg' % (pot, picName)

        allList.append([picName, pic])

dSet = {x.replace('.jpg', '') for x in os.listdir('images')}
allList = [x for x in allList if x[0].replace('.jpg', '') not in dSet and 'http' in x[1] and '.jpe' in x[1]]

#asdfsad
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(get, allList, timeout=15)





