# encoding:utf-8
# @CreateTime: 2022/1/18 15:01
# @Author: Xuguangchun
# @FlieName: newsInfo.py
# @SoftWare: PyCharm

import requests
import re
import time
import csv
import traceback
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


# option = Options()  # 实例化option对象
# option.add_argument("--headless")  # 给option对象添加无头参数

# if __name__ == '__main__':
#     web = Chrome(executable_path='D:\pachong_2022\\venv\chromedriver.exe', options=option) # 指定驱动位置,否则从python解释器目录下查找.
#     web.get("https://www.beritasatu.com/")
#     last_height = web.execute_script("return document.body.scrollHeight")
#     # print(web.page_source)
#     print(last_height)


# 第一步先获取网页,第二步解析网页提取数据，第三步写入

class GetNewsInfo(object):
    def __init__(self):
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = Chrome(executable_path='D:\\pachong_2022\\venv\\chromedriver.exe', options=self.option)

    def get_page(self, num):
        flag = 0
        page = 0
        url = 'https://www.beritasatu.com/megapolitan'
        self.driver.get(url=url)
        # 返回当前的网页的高度
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        csv_file = open('D:\\idNews.csv', 'wt', newline='', encoding='utf-8')  # newline='',
        writer = csv.writer(csv_file)
        writer.writerow(['newsTitle', 'newsFuTitle', 'newsArea', 'newsTime', 'newsLink', 'picLink'])
        try:
            while page < num:
                page += 1
                # 滑动一次
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 等待加载
                time.sleep(5)
                # 计算新的滚动高度并与上一个滚动高度进行比较
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break
                last_height = new_height
                print('目前滑动第%d页\n现在高度为:%d，url==>%s' % (page, new_height, url))
            html = self.driver.page_source
            soup = bs(html, 'html.parser')
            picList = []

            for pic in soup.find_all('div', class_='col-4'):
                if pic.find_all('div', class_='img-thumb-5') is not None:
                    picLink = str(pic.find_all('div', class_='img-thumb-5'))
                    picLink = (re.findall(r'https*://.+\.*g', picLink))
                    picList.append(picLink)
            print('新闻封面============>', picList)

            for news in soup.find_all('div', class_='col pl-0'):
                if news.find('p', class_='text-muted') is not None:
                    flag += 1
                    newsLink = news.a['href']
                    newsTitle = news.find('a', class_='black').text
                    newsFuTitle = news.find('p', class_='text-muted').text
                    newsArea = news.find('a', class_='red').text
                    newsTime = news.find('div', class_='small').text
                    newsTime = newsTime.split('|')[1]
                    # picLink = ''
                    print('<这个是最新新闻第%d条>：newsLink============>%s' % (flag, newsLink))
                    print('主标题============>', newsTitle)
                    print('副标题============>', newsFuTitle)
                    print('新闻地点============>', newsArea)
                    print('新闻时间============>', newsTime)
                    writer.writerow([newsTitle.strip('\xa0'), newsFuTitle.strip('\xa0'), newsArea.strip('\xa0'),
                                     newsTime.strip('\xa0'), newsLink.strip('\xa0'), picList[flag - 1][0]])
                    # csv_file.close()
                    # read_csv = open('D:\\idNews.csv', 'r')
                    # reader_file = csv.reader(read_csv)
                    # for pic in soup.find_all('div', class_='col-4'):
                    #     read_csv = open('D:\\idNews.csv', 'r')
                    #     reader_file = csv.reader(read_csv)
                    #     if pic.find_all('div', class_='img-thumb-5') is not None:
                    #         picLink = str(pic.find_all('div', class_='img-thumb-5'))
                    #         picLink = (re.findall(r'https*://.+\.*g', picLink))[0]
                    #         print('新闻封面============>', picLink)
                    #         csv_file2 = open('D:\\idNews.csv', 'a', encoding='utf-8')
                    #         writer2 = csv.writer(csv_file2)
                    #         for row in reader_file:
                    #             print('这是：row=====>', row)
                    #             if row[5] == 'picLink':
                    #                 continue
                    #                 row[5] = picLink
                    #                 csv_file2 = open('D:\\idNews.csv', 'a', encoding='utf-8')
                    #                 writer2 = csv.writer(csv_file2)
                    #                 writer2.writerow(row)
        except:
            traceback.print_exc()
            return '爬取失败'


if __name__ == '__main__':
    getPage = GetNewsInfo()
    getPage.get_page(1)

"""
    # lastid规则无法获取，作废
    # getPage.get_page(5)
    # for page in range(nums):
    #     fl += 1
    #     page += 1
    #     url = 'https://www.beritasatu.com/listing/getListing?param=megapolitan&page=' + str(
    #         page - 1) + '&lastid=880885'
    #     # 'https://www.beritasatu.com/listing/getListing?param=megapolitan&page=1&lastid=880801'
    #     # 访问请求头
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    #     r = requests.get(url, headers=headers)
    #     r.encoding = 'utf-8'
"""
