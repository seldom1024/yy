import requests
from bs4 import BeautifulSoup
import xlwt
import re
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.cnki.net',
    'Referer': 'http://search.cnki.net/search.aspx?q=%E4%BD%9C%E8%80%85%E5%8D%95%E4%BD%8D%3a%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6&rank=relevant&cluster=zyk&val=CDFDTOTAL',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

if __name__ == '__main__':
    # start = time.clock()
    start = time.perf_counter()
# 读取已经获得的文章链接
file = open('data-detail.txt', encoding="utf-8")

# xls创建与写入
wb = xlwt.Workbook('data_out.xsl')
sheet = wb.add_sheet('data-out')
sheet.write(0, 0, '网址')
sheet.write(0, 1, '标题')
sheet.write(0, 2, '作者')
sheet.write(0, 3, '机构')
sheet.write(0, 4, '摘要')
sheet.write(0, 5, '关键词')

lin_num = 1
txt_num = 1

for href in file:
    if re.match(r'^(http://www.cnki.com.cn/Article/CJFDTOTAL)-\w{4}(\w*)', href):
        year = href[-14:-10]
        name = href[-18:-5]
        # 含关键词的详情页链接
        paper_url = "http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST" + year + "&filename=" + name
        try:

            html = requests.get(paper_url, headers=headers, timeout=500)
            soup = BeautifulSoup(html.text, 'html.parser')

        except:
            print("No result")
            break

        # 获取标题
        title = soup.find('h2', class_='title').get_text()

        # 获取作者
        # author = soup.find('div', class_='author').get_text() 比较简单，但是作者姓名容易黏在一起
        author = ''
        for a in soup.find('div', class_='author').children:
            author += (a.get_text() + ';')

        # 获取机构
        orgn = soup.find('div', class_='orgn').get_text()

        # 获取摘要
        abstract = soup.find('span', id='ChDivSummary').get_text()

        # 获取关键词，存在没有关键词的情况
        try:
            key = ''
            for k in soup.find('label', id='catalog_KEYWORD').next_siblings:
                ke = (k.get_text()).strip()
                key += ke.replace('\r\n', '')
        except:
            pass

        print(title)

        line = paper_url + '\t' + str(title) + '\t' + str(author) + '\t' + str(orgn) + '\t' + str(
            abstract) + '\t' + str(key) + '\n'
        outstring = line.split('\t')
        for i in range(len(outstring)):
            # 写入
            sheet.write(lin_num, i, outstring[i])
        print('写入第' + str(lin_num) + '行')
        lin_num += 1

        # 保存成xx文件
        wb.save('data_out_' + str('大数据' + '.xls'))

file.close()
end = time.clock()
print('完成论文数据获取共用时：%s Seconds' % (end - start))
