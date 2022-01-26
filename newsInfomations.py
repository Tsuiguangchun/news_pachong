# encoding:utf-8
# @CreateTime: 2022/1/24 17:11
# @Author: Xuguangchun
# @FlieName: newsInfomations.py
# @SoftWare: PyCharm

import re
from bs4 import BeautifulSoup as bs
from getPageSource import *
from connect_mysql import *
import time
# from datetime import datetime


class GetNews(object):
    def __init__(self):
        self.flag = 0
        self.Mysql = OperationMysql()
        self.Mysql.delete_db(mysql='delete from news')

    # 封装整个网站解析提取数据方法
    def getSource(self, url, typeNum, endPageNumber):
        timestamp = int(time.time())
        pageSource = getPageSource(num=endPageNumber, url=url)
        soup = bs(pageSource, 'html.parser')

        # writer = writerIn(filePath=filePath) #这个写入csv的，后面改成数据库存储
        # writer.writerow(['newsTitle', 'newsFuTitle', 'newsArea', 'newsTime', 'newsLink', 'picLink'])
        picList = []

        for pic in soup.find_all('div', class_='col-4'):
            if pic.find_all('div', class_='img-thumb-5') is not None:
                picLink = str(pic.find_all('div', class_='img-thumb-5'))
                picLink = (re.findall(r'https*://.+\.*g', picLink))  # 提取出来是个列表
                picList.append(picLink)
        # print('新闻封面============>', picList)

        for news1 in soup.find_all('div', class_='col pl-0'):
            if news1.find('p', class_='text-muted') is not None:
                self.flag += 1
                newsLink = news1.a['href']
                newsTitle = news1.find('a', class_='black').text
                newsFuTitle = news1.find('p', class_='text-muted').text
                newsArea = news1.find('a', class_='red').text
                newsTime = news1.find('div', class_='small').text
                newsTime = newsTime.split('|')[1]
                # picLink = ''
                print('<这个是最新新闻第%d条>：newsLink============>%s' % (self.flag, newsLink))

                news_sql = 'insert into news values(null,%s, %s, %s, %s, %s, %s, %s, %s, %s,null)'
                title = newsTitle.strip('\xa0')
                fu_title = newsFuTitle.strip('\xa0')
                url = newsLink
                pic_url = picList[self.flag - 1][0]
                type = typeNum
                created_at = timestamp
                update_at = timestamp
                news_address = newsArea.strip('\xa0')
                news_time = newsTime.strip('\xa0')
                values = (title, fu_title, url, pic_url, type, created_at, update_at, news_address, news_time)
                self.Mysql.insert_db(mysql=news_sql, values=values)

                # writer.writerow([newsTitle.strip('\xa0'), newsFuTitle.strip('\xa0'), newsArea.strip('\xa0'),
                #                  newsTime.strip('\xa0'), newsLink.strip('\xa0'), picList[self.flag - 1][0]])

    # 大都会
    def daDuHui(self):
        url = 'https://www.beritasatu.com/megapolitan'
        # filePath = 'D:\\idNews.csv'
        GetNews().getSource(url=url, typeNum=1, endPageNumber=5)

    # 国家
    def country(self):
        url = 'https://www.beritasatu.com/nasional'
        # filePath = 'D:\\country.csv'
        GetNews().getSource(url=url, typeNum=2, endPageNumber=5)

    # 群岛
    def qunDao(self):
        url = 'https://www.beritasatu.com/nasional/nusantara'
        # filePath = 'D:\\qunDao.csv'
        GetNews().getSource(url=url, typeNum=3, endPageNumber=5)

    # 经济
    def economics(self):
        url = 'https://www.beritasatu.com/ekonomi'
        # filePath = 'D:\\economics.csv'
        GetNews().getSource(url=url, typeNum=4, endPageNumber=5)

    # 运动
    def sport(self):
        url = 'https://www.beritasatu.com/olahraga'
        # filePath = 'D:\\sport.csv'
        GetNews().getSource(url=url, typeNum=5, endPageNumber=5)

    # 球
    def bola(self):
        url = 'https://www.beritasatu.com/bola'
        # filePath = 'D:\\bola.csv'
        GetNews().getSource(url=url, typeNum=6, endPageNumber=5)

    # 科学与技术（数字）
    def digit(self):
        url = 'https://www.beritasatu.com/digital'
        # filePath = 'D:\\digit.csv'
        GetNews().getSource(url=url, typeNum=7, endPageNumber=5)

    # 生活方式
    def lifeStyle(self):
        url = 'https://www.beritasatu.com/gaya-hidup'
        # filePath = 'D:\\lifeStyle.csv'
        GetNews().getSource(url=url, typeNum=8, endPageNumber=5)

    # 健康
    def healthy(self):
        url = 'https://www.beritasatu.com/kesehatan'
        # filePath = 'D:\\healthy.csv'
        GetNews().getSource(url=url, typeNum=9, endPageNumber=5)

    # 娱乐
    def yuLe(self):
        url = 'https://www.beritasatu.com/hiburan'
        # filePath = 'D:\\yuLe.csv'
        GetNews().getSource(url=url, typeNum=10, endPageNumber=5)

    # 汽车
    def car(self):
        url = 'https://www.beritasatu.com/otomotif'
        # filePath = 'D:\\car.csv'
        GetNews().getSource(url=url, typeNum=11, endPageNumber=5)


if __name__ == '__main__':
    news = GetNews()
    news.daDuHui()
    news.country()
    news.economics()
    news.sport()
    news.bola()
    news.healthy()
    news.lifeStyle()
    news.car()
    news.digit()
    news.qunDao()
    news.yuLe()
