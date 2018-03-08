# -*- coding: utf-8 -*-
# @Time    : 2018/2/10 18:33
# @Author  : 陈强
# @FileName: genUserTag.py
# @Software: PyCharm

"""根据用户行为更新用户兴趣表"""

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from news.models import news_tag_score
from user.models import user_tag_score
from django.forms import model_to_dict

class UserTag():
    """
    user_tag_score+=news_tag_score*behavior_type*behavior_way
    用户阅读的资讯的分数*行为类型（1.仅阅读；2.点赞；-1：不喜欢；-2：阅读后点踩）*阅读方式（1.通过推荐；2.搜索，说明其主动对该资讯感兴趣）
    """

    """根据用户对某条新闻产生的行为类型来更新他的兴趣表"""
    def __init__(self,news_id,user_id,behavior_type=1,behavior_way=1):
        self.news_id = news_id
        self.user_id = user_id
        self.behavior_type = behavior_type
        self.behavior_way = behavior_way

    def calculate(self):
        user_score = user_tag_score.objects.get(user_id=self.user_id)
        news_score = news_tag_score.objects.get(news_id=self.news_id)

        user_dict = model_to_dict(user_score,exclude=['user'])
        news_dict = model_to_dict(news_score,exclude=['news'])

        for i in news_dict:
            temp = news_dict[i]
            news_dict[i] = temp*self.behavior_type*self.behavior_way

        for i in news_dict:
            user_dict[i] += news_dict[i]

        user_dict['user_id'] = self.user_id

        user_tag_score.objects.filter(user_id=self.user_id).update(**user_dict)


if __name__=='__main__':
    UserTag(1,2).calculate()


