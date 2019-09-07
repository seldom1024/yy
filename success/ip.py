# coding=utf8
import requests
from bs4 import BeautifulSoup
import re

ip_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
ip_headers = {'User-Agent': ip_user_agent}

def getListProxies():
    session = requests.session()
    page = session.get("http://www.xicidaili.com/nn", headers=ip_headers)
    soup = BeautifulSoup(page.text, 'lxml')
    proxyList = []
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        tdlist = trtag.find_all('td')
        proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,
                 'https': tdlist[1].string + ':' + tdlist[2].string}
        proxyList.append(proxy)
        # 设定代理ip个数
        if len(proxyList) >= 10:
            break
    return proxyList


res = getListProxies()
print(type(res))
print(res)
