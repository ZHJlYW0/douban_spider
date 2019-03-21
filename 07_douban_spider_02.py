# coding=utf-8
import json

import requests

from parse import parse_url


class DoubanSpider(object):
    def __init__(self):
        self.temp_url = 'https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?os=android&for_mobile=1&start={}&count=18&loc_id=108288&_=0'  # 删除【&callback=jsonp1】

    def get_data(self, html_str):
        """3 提取数据"""
        html_dict = json.loads(html_str)
        count = html_dict['count']
        start = html_dict['start']
        subject_collection_items = html_dict['subject_collection_items']
        total = html_dict['total']
        return count, start, subject_collection_items, total

    def save_data(self, subject_collection_items):
        # with open的缺点：每写入一页，都要开关一次文件，浪费资源
        with open('douban2.csv', 'w+', encoding='utf-8') as f:
            for i in subject_collection_items:
                f.write(json.dumps(i, ensure_ascii=False, ))
                f.write(',\n')
        print('保存成功')

    def run(self):
        """实现主要逻辑"""
        start = 0
        # count = 18
        # total = 18
        # while start <= total:  # 循环1～5；total=50
        # while start < total + count:  # 循环1～5；total + count = 68
        while True:
            print(start)  # 0 --> 18 --> 36 --> 54
            """
            url：统一资源定位器
            1 起始的url：start_url
            2 发送请求，获取响应
            3 提取数据
            4 保存
            5 构造下一页的起始url地址：start_url
            6 循环1～5
            """
            # 1 起始的统一资源定位器：start_url
            start_url = self.temp_url.format(start)

            # 2 发送请求，获取响应
            html_str = parse_url(start_url)
            """
            request_headers = {"Referer": "https://m.douban.com/tv/",
                               "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Mobile Safari/537.36"}
            response = requests.get(start_url, headers=request_headers)
            html_str = response.content.decode()
            """

            # 3 提取数据
            count, start, subject_collection_items, total = self.get_data(html_str)

            # 4 保存
            self.save_data(subject_collection_items)

            # 5 构造下一页的url地址
            start += count

            # 6 判断是否继续循环
            if start > total + count:
                break


if __name__ == '__main__':
    douban = DoubanSpider()
    douban.run()

"""
0
尝试执行次数：1
保存成功
18
尝试执行次数：2
保存成功
36
尝试执行次数：3
保存成功
54
尝试执行次数：4
保存成功
"""
