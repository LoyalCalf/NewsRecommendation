# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 15:10
# @Author  : 陈强
# @FileName: HotNews.py
# @Software: PyCharm

"""
热点资讯算法，返回不同类型下的热点新闻
"""
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from news.models import news,news_profile,news_hot
from datetime import datetime,timedelta


class HotNews(object):
    """
    (总浏览*0.6+总评论数*0.2+总喜欢数*0.2)*1000/(发布时间距离当前时间的小时差+2)^1.2
    每隔一段时间（比如一小时）更新热点新闻表
    """
    #不同类型的热点资讯
    # def __init__(self,classification):
    #     self.classification=classification


    def get_days_before_today(self,hours=16):
        return datetime.now() - timedelta(hours=hours)

    # def get_data(self,delta_hours):
    #     news_id_list = news.objects.filter(pubtime__gte=self.get_days_before_today(delta_hours)).values_list('news_id',flat=True)
    #
    #     return news_id_list

    # def update_data(self,dic):
    #     hot_news = news_hot.objects.filter(news_id=dic['news_id'])
    #     if hot_news.exists():
    #         news_hot.objects.up
    #     pass

    def score(self,viewed_count,comment_count,liked_count,delta_time):

        return (viewed_count*0.6+comment_count*0.2+liked_count*0.2)*1000/(delta_time+2)**1.2


    def calculate_hot_news(self):

        news_id_list = news.objects.filter(pubtime__gte=self.get_days_before_today()).values_list('news_id',flat=True)
        news_profile_query = news_profile.objects.filter(news_id__in=news_id_list)
        for i in news_profile_query:
            delta_time = datetime.now()-i.pubtime
            score = self.score(i.viewed_count,i.comment_count,i.liked_count,float(delta_time.seconds)/3600)
            dic = {'news_id':i.news_id,'score':score,'pubtime':i.pubtime}
            news_hot.objects.update_or_create(**dic)


if __name__=='__main__':

    HotNews().calculate_hot_news()


