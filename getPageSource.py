# encoding:utf-8
# @CreateTime: 2022/1/24 15:23
# @Author: Xuguangchun
# @FlieName: getPageSource.py
# @SoftWare: PyCharm
import csv
import time
import traceback

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

"""
封装获取网页信息返回给其他模块重复调用
# 实例化Options()对象
# option.add_argument("--headless")给option对象添加无头参数
# driver创建浏览器驱动对象
# 通过判断浏览器高度进行滑动，如果写成死循环最后一次高度等于上一次高度，停止爬取
"""


def getPageSource(num, url):
    page = 0
    option = Options()
    option.add_argument("--headless")
    driver = Chrome(executable_path='D:\\pachong_2022\\venv\\chromedriver.exe', options=option)
    driver.get(url=url)
    # 返回当前的网页的高度
    last_height = driver.execute_script("return document.body.scrollHeight")

    try:
        while page < num:
            page += 1
            # 滑动一次
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 等待加载
            time.sleep(5)
            # 计算新的滚动高度并与上一个滚动高度进行比较
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height
            print('目前滑动第%d页\n现在高度为:%d，url==>%s' % (page, new_height, url))
        html = driver.page_source
        return html
        # soup = bs(html, 'html.parser')
    except:
        traceback.print_exc()
        return '爬取失败'


def writerIn(filePath):
    csv_file = open(filePath, 'wt', newline='', encoding='utf-8')  # newline='',
    writer = csv.writer(csv_file)
    return writer
