# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:38:46 2018

@author: Ureridu
"""



import requests
from lxml import html
import pandas as pd
import time

url1 = 'https://www.beazley.ox.ac.uk/XDB/ASP/searchOpen.asp?action=showResults&search=%20%7BAND%7D%20%20%5BWith%20Images%5D%20Yes&startFrom='
url2 = '&noToDisplay='
url3 = '&setResultCheckboxes=chkTextDetailed&chkImages=false&chkImagesAll=true&chkText=true&chkTextDetailed=true&chkMap=false&chkTimeline=false&chkAlbum=false&sid=0.3611978315516611'
numDisp = 1000

headers = {
            'authority': 'www.beazley.ox.ac.uk',
            'method': 'GET',
            'path': '/XDB/ASP/searchOpen.asp?action=showResults&search=%20{AND}%20%20[With%20Images]%20Yes&startFrom=51&noToDisplay=50&returnFrame=divMore51&sid=0.7954203882841406',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'ASPSESSIONIDAQQQBDDC=FNGMBPDCELLLMCMCDOEOFOJN; _ga=GA1.3.1795321356.1528680275; _gid=GA1.3.149711345.1528680275; XDBSession=SessionGUIDXDBSession=%7BC3432221%2DA5A3%2D46B7%2DBABA%2D33956F514E92%7D; ASPSESSIONIDAUQQBDDC=JBKMBPDCLEMPHCJIBEJPIKJJ; MostRecentSession=LastLaunchPage=%2FXDB%2FASP%2Fdefault%2Easp; _gat=1; cookiesDisclosureCount=44',
            'pragma': 'no-cache',
            'referer': 'https://www.beazley.ox.ac.uk/XDB/ASP/searchOpen.asp',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36}',
            }
bad = []
final = pd.DataFrame()

for num in range(67434)[::1000]:
    print(num)
    time.sleep(1)
    url = url1 + str(num) + url2 + str(numDisp) + url3
    while 1:
        bc = 0
        try:
            r = requests.get(url, headers=headers)
        except:
            bc +=1
        if r.status_code != 200:
            bc += 1
        else:
            break
        if bc >=3:
            bad.append(url)

    text = r.text

    if text:
        body = html.fromstring(text)

        results = body.xpath('//div[@class="searchResultTable"]')
        print(len(results))

        data = pd.DataFrame()

        for i, res in enumerate(results):

            try:
                inner = pd.DataFrame([[None, None, None]], columns=['Data', 'Text', 'Pics'])

                inner['Data'] = res.xpath('.//div')[0].attrib['onclick']
                nodes = res.xpath('.//div[@class="searchResultCell"]/div')
                inner.at[0, 'Text'] = nodes[-1].text_content()
                inner.at[0, 'Pics'] = []

                for nod in nodes[:-1]:
                    n = nod.xpath('.//img')[0]
                    inner.at[0, 'Pics'].append('https://www.beazley.ox.ac.uk' + n.attrib['src'])

                data = pd.concat([data, inner])
            except Exception as e:
                print(e)

        final = pd.concat([final, data])
    else:
        bad.append(url)


with pd.ExcelWriter('Pots.xlsx') as writer:
    final.to_excel(writer)