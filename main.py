# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

#爬虫没爬出来
def search(url):
    headers1 = {
    ':authority' : 'olympics.com' ,
    ':method' : 'GET' ,
    ':path' : '/zh/olympic-games/beijing-2022/results/nordic-combined/individual-gundersen-large-hill-10km ' ,
    ':scheme' : 'https' ,
    'accept' : 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
    'accept - encoding' : 'gzip, deflate, br',
    'accept - language' : 'zh - CN, zh; q = 0.9, en - US; q = 0.8, en; q = 0.7',
    'cache - control' : 'max - age = 0',
    #'if -none - match' : "m6n3135m6uizz3",
    'sec - ch - ua' : '".Not/A)Brand"; v = "99", "Google Chrome"; v = "103", "Chromium";v = "103"',
    'sec - ch - ua - mobile': '?0',
    'sec - ch - ua - platform': '"Windows"',
    'sec - fetch - dest' : 'document',
    'sec - fetch - mode' : 'navigate',
    'sec - fetch - site': 'same - origin',
    'sec - fetch - user' : '?1',
    'upgrade - insecure - requests': '1',
    'user - agent': 'Mozilla / 5.0(WindowsNT10.0; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 103.0.0 .0 Safari / 537.36'
    }
    try:
       r = requests.request(url, headers=headers1)
       r.raise_for_status()
       r.encoding = 'utf-8'
       return r.text
    except:
       print("无法连接")

if __name__ == '__main__':
    url = "https://olympics.com/zh/olympic-games/beijing-2022/results/nordic-combined/individual-gundersen-large-hill-10km"
    test=search(url)
    print(test)

