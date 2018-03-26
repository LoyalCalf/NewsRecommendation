# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 15:51
# @Author  : 陈强
# @FileName: Novel.py
# @Software: PyCharm

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from user.models import user_tag_score,user_novel_recommendation
from news.models import news_tag_score,news
import numpy as np
from datetime import datetime, timedelta


"""新奇推荐，推荐用户阅读较少的内容"""

class NovelRecommendation(object):

    hours = 6
    news_tag_list = []

    def __init__(self):
        pass

    def get_days_before_today(self):
        return datetime.now() - timedelta(hours=self.hours)

    def get_news(self):
        news_list = news.objects.filter(pubtime__gte=self.get_days_before_today())
        for i in news_list:
            self.news_tag_list.append(i.news_tag)


    def cosine_similarity(self, x, y):
        num = sum(np.multiply(np.array(x), np.array(y)))
        denom = np.linalg.norm(x) * np.linalg.norm(y)
        return round(num / float(denom), 3)

    def get_data(self):
        users_tag = user_tag_score.objects.all()

    def calculate(self,user):
        pass



