# -*- coding: utf-8 -*-
# @Author  : Felix
# @Function: 爬取南京工程学院星火新闻网（http://xinghuo.njit.edu.cn/）近期新闻，并存入csv

from bs4 import BeautifulSoup
import requests
import re
import csv
import time

#获取页码
def get_page(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    page = int(soup.find(id="fanye201208").get_text().split("/")[1])
    return page

#获取单个页面上所有url
def get_url_onepage(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(href=re.compile("info/[0-9]*/[0-9]*"))
    main_url = 'http://xinghuo.njit.edu.cn/'
    url_lists = []
    for link in links:
        url_lists.append(main_url+re.findall("info/[0-9]*/[0-9]*.htm",link['href'])[0])
    return url_lists

#获取指定页码范围内所有url
def get_url(url):
    page = get_page(url)
    url_lists = get_url_onepage(url)
    page_urls = []
    for i in range(page-1,page-21,-1): #调整range()的第二个数值，以达到爬取指定页码范围的目标
        page_urls.append('{}/{}.htm'.format(url[:-4],i))
    for page in page_urls:
        url_lists.extend(get_url_onepage(page))
    return url_lists

#获取内容
def get_content():
    urls = ['http://xinghuo.njit.edu.cn/xyyw.htm','http://xinghuo.njit.edu.cn/zhxw.htm']
    data = []
    for u in urls:
        for url in get_url(u):
            r = requests.get(url)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find_all('h1')[1].get_text()
            pub_date = list(soup.find('h2').children)[0][3:]
            pub_person = list(soup.find('h2').children)[1].get_text()[4:]
            if soup.find(id="vsb_content_500") is None:
                content = None
            else:
                content = list(soup.find(id="vsb_content_500").children)[0].get_text()
            record = (url,title,pub_date,pub_person,content)
            data.append(record)
    return data

#写入csv文件
def write_to_csv(data):
    csvfile = open('news.csv', 'w+',newline='',encoding='utf8')
    writer = csv.writer(csvfile)
    writer.writerow(['url','title','date','publisher','content'])
    writer.writerows(data)
    csvfile.close()

if __name__ == '__main__':
    start_time = time.time()
    data = get_content()
    write_to_csv(data)
    end_time = time.time()
    print("运行时间：{}(s)\n爬取信息条数：{}\n运行速率：{}(条/s)"
          .format((end_time-start_time),len(data),len(data)/(end_time-start_time)))