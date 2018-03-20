# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 15:01
# @Author  : 陈强
# @FileName: HotSearch.py
# @Software: PyCharm

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from user.models import user_search
from news.models import search_hot
from datetime import datetime, timedelta
import jieba

"""
热门搜索算法
"""


class HotSearch(object):
    def __init__(self, hours):
        self.hours = hours
        self.words_set = self.MakeWordsSet('../NaiveBayes/stop_words.txt')
        self.words_count = {}

    def get_days_before_today(self):
        return datetime.now() - timedelta(hours=self.hours)

    # 停词表
    def MakeWordsSet(self, words_file):
        words_set = set()  # 创建set集合
        with open(words_file, 'r', encoding='utf-8') as f:  # 打开文件
            for line in f.readlines():  # 一行一行读取
                word = line.strip()  # 去回车
                if len(word) > 0:  # 有文本，则添加到words_set中
                    words_set.add(word)
        return words_set  # 返回处理结果

    def count_words(self):
        # 取出最新的搜索内容
        res = user_search.objects.filter(date_created__gte=self.get_days_before_today())
        for i in res:
            # jieba_content = re.sub(r'[0-9]+', '', i.content)  # 去掉数字，避免数字被提为关键字
            tags = jieba.cut(i.content, cut_all=False)
            for tag in tags:
                if not tag.isdigit() and tag not in self.words_set:
                    if tag in self.words_count:
                        self.words_count[tag] += 1
                    else:
                        self.words_count[tag] = 1
        self.update_data()

    def update_data(self):
        for words, count in self.words_count.items():
            dic = {'key_words': words, 'count': count}
            search_hot.objects.create(**dic)


if __name__ == '__main__':
    HotSearch(6).count_words()
