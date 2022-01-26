# encoding:utf-8
# @CreateTime: 2022/1/18 11:05
# @Author: Xuguangchun
# @FlieName: gangjiwang.py
# @SoftWare: PyCharm

import requests
import csv
import traceback
from bs4 import BeautifulSoup as bs


# 第一步先获取网页
def get_page():
    try:
        url = 'https://gz.ganji.com/ruanjiangong/'
        # 访问请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        print('这是爬取网页原内容：===========》\n', r.text)
        return r.text
    except:
        traceback.print_exc()
        return "爬取失败"


# 第二步开始解析网页并找到所需信息
def get_page_parse(html):
    # 打开文件设置好格式
    csv_file = open('D:\\data.csv', 'wt', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['职位', '公司', '地点', '薪水', '福利'])
    content = []
    # 开始解析网页源码，获取数据
    soup = bs(html, 'html.parser')
    for dl in soup.find_all('div', class_='ibox'):
        job = dl.find('li', class_="ibox-title").text  # 职位
        company = dl.find('li', class_='ibox-enterprise').text  # 公司
        aDress = dl.find('li', class_='ibox-address').text  # 招聘地址
        Salary = dl.find('li', class_='ibox-salary').text  # 岗位薪资
        Welfare = dl.find('span', class_='ibox-icon-item').text  # 福利

        # print('==================DIV++++++=====>>>>>\n', dl)
        # print('==================attrs++++++=====>>>>>\n', dl.attrs)
        print('==================JOB++++++=====>>>>>\n', job)
        print('==================company++++++=====>>>>>\n', company)
        print('==================Salary++++++=====>>>>>\n', Salary)
        print('==================aDress++++++=====>>>>>\n', aDress)
        print('==================Welfare++++++=====>>>>>\n', Welfare)

        writer.writerow([job, company, aDress, Salary, Welfare])
    csv_file.close()
    print('所有数据成功放入CSV中')


# 主函数：
if __name__ == '__main__':
    html = get_page()
    get_page_parse(html)
