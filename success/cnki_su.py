import requests
from bs4 import BeautifulSoup
import time
import xlwt

firsturl = "http://kns.cnki.net/kns/request/SearchHandler.ashx"

wantsearch = input()


def ToUtf(string):
    return string.encode('utf8')

times = time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'
headers2 = {'action': '',
            'ua': '1.11',
            'isinEn': '1',
            'PageName': 'ASP.brief_default_result_aspx',
            'DbPrefix': 'SCDB',
            'ConfigFile': 'SCDBINDEX.xml',
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            'txt_1_sel': 'SU$%=|',
            'txt_1_value1': wantsearch,
            'txt_1_special1': '%',
            'his': '0',
            'parentdb': 'SCDB',
            '__': times}
headers = {'Connection': 'Keep-Alive',
           'Accept': 'text/html,*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
           'Referer': "http://kns.cnki.net/kns/brief/default_result.aspx",
           'Cookie': 'Ecp_ClientId=4190902163101077574; cnkiUserKey=b3ef499b-83eb-5bf6-4a3d-7fb0628c2718; UM_distinctid=16cfd0a11ba17f-07ed3c0e494639-c343162-1fa400-16cfd0a11bb2b3; LID=WEEvREcwSlJHSldRa1FhdkJkVG1EREREYzZRbUJ4aW0vMExjUytxakRLYz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; ASP.NET_SessionId=0vs22otfl20z10wzxomi1bem; SID_kns=123121; SID_klogin=125141; Ecp_session=1; SID_crrs=125134; KNS_SortType=; SID_krsnew=125131; SID_kcms=124105; RsPerPage=10; _pk_ref=%5B%22%22%2C%22%22%2C1567726281%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*',
           }
header = {'Connection': 'Keep-Alive',
          'Accept': 'text/html,*/*',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
          'Referer': "http://kns.cnki.net/kns/brief/default_result.aspx?code=SCDB",
          'Cookie': 'Ecp_ClientId=4190902163101077574; cnkiUserKey=b3ef499b-83eb-5bf6-4a3d-7fb0628c2718; UM_distinctid=16cfd0a11ba17f-07ed3c0e494639-c343162-1fa400-16cfd0a11bb2b3; LID=WEEvREcwSlJHSldRa1FhdkJkVG1EREREYzZRbUJ4aW0vMExjUytxakRLYz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; ASP.NET_SessionId=0vs22otfl20z10wzxomi1bem; SID_kns=123121; SID_klogin=125141; Ecp_session=1; SID_crrs=125134; KNS_SortType=; SID_krsnew=125131; SID_kcms=124105; RsPerPage=10; _pk_ref=%5B%22%22%2C%22%22%2C1567726281%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*',
          }
firstmagess = requests.get(firsturl, headers=headers, data=headers2).text
secondurl = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=" + str(firstmagess) + "&S=1&sorttype="


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

for k_p in range(30):
    thirdurl = 'http://kns.cnki.net/kns/brief/brief.aspx?' \
               'curpage=' + str(k_p) + '&RecordsPerPage=10&QueryID=6&ID=&turnpage=1' \
               '&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&isinEn=1&'
    secondhtml = requests.get(thirdurl, headers=headers).text
    # print(secondhtml)
    secondhtml = BeautifulSoup(secondhtml, "lxml")
    html = secondhtml.select("td a[target='_blank']")

    p = 0

    for i in html:
        # print(i)
        if p % 3 == 0:
            href = i['href']
            year = href[64:68]
            dbcode = href[99:103]
            dbname = href[83:91]
            filename = href[60:75]
            # 含关键词的详情页链接
            paper_url = "http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=" + dbcode + "&dbname=" + dbname + year + "&filename=" + filename

            try:

                html = requests.get(paper_url, headers=headers, timeout=500)
                soup = BeautifulSoup(html.text, 'html.parser')

            except:
                print("No result")
                continue

            # print(soup)

            # 获取标题
            try:
                title = soup.find('h2', class_='title').get_text()
            except:
                continue

            # 获取作者
            # author = soup.find('div', class_='author').get_text() 比较简单，但是作者姓名容易黏在一起
            author = ''
            for a in soup.find('div', class_='author').children:
                author += (a.get_text() + ';')

            # 获取机构
            try:
                orgn = soup.find('div', class_='orgn').get_text()
            except:
                continue

            # 获取摘要
            try:
                abstract = soup.find('span', id='ChDivSummary').get_text()
            except:
                continue

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
            wb.save('data_out_' + str(wantsearch + '.xls'))

        p = p + 1
        time.sleep(10)
    print("第"+str(k_p)+"页完成")

