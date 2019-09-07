# -*- coding:utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import math
import io
import time
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

if __name__ == '__main__':
    # 获取开始时间
    # start = time.clock()
    start = time.perf_counter()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    # 避免之前的内容重复爬取
    if os.path.exists('data-detail.txt'):
        print("存在输出文件，删除文件")
        os.remove('data-detail.txt')

# 获取页数，可以根据搜索关键词进行url修改，这里是“大数据”
index_url = r'http://search.cnki.com.cn/Search.aspx?q=大数据&rank=relevant&cluster=zyk&val=CJFDTOTAL'
htm1 = requests.get(index_url, headers=headers)
soup = BeautifulSoup(htm1.text, 'html.parser')
pagesum_text = soup.find('span', class_='page-sum').get_text()
maxpage = math.ceil(int(pagesum_text[7:-1]) / 15)
print('The total page is:', maxpage)

# 获取各检索结果文章链接
for i in range(0, maxpage):
    page_num = 15  # 一页共有15条搜索结果
    url = index_url + '&p=' + str(i * page_num)  # 构建url链接

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        break

    f = open('data-detail.txt', 'a+', encoding='utf-8')
    all = soup.find_all('div', class_='wz_content')
    for string in all:
        item = string.find('a', target='_blank')  # 文章标题与链接
        href = item.get('href')  # 获取文章链接
        # title=item.get_text()#获取文章标题
        f.write(href + '\n')

    f.close()

    # 获取结束时间
    # end = time.clock()
    end = time.perf_counter()
    print('获取文章详情页链接共用时：%s Seconds' % (end - start))
