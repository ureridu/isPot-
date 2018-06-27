# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 20:09:57 2018

@author: Ureridu
"""


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
            }

cookies = {}


class Requester():
    def __init__(self, proxy=True, headers=headers, cookies=cookies, fails=5, verify=False):
        self.headers = headers
        self.cookies = cookies
        self.verify = verify
        self.fails = fails

        proxy_host = "proxy.crawlera.com"
        proxy_port = "8010"
        proxy_auth = "f93f7d78647b4db3b8b4e112fff9492c:"

        if proxy:
            self.proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                            "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
        else:
            self.proxies = None

    def request(self, url, data=None, req='get'):
        if req == 'get':
            doer = requests.get
        elif req == 'post':
            doer = requests.post

        bc = 0
        while 1:
            try:
#                print(url)
                r = doer(url,
                         headers=self.headers,
                         cookies=self.cookies,
                         data=data,
                         proxies=self.proxies,
                         verify=self.verify)
            except Exception as e:
                print(e)
                bc += 1

            if r.status_code == 200 or bc >= self.fail:
                return r
            else:
                bc += 1


    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)


#url = 'http://httpbin.org/ip'
#x = Requester()
#t = x(url)
#print(t.text)