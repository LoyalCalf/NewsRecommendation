# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 13:56
# @Author  : 陈强
# @FileName: models.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import User
from news.models import news


# class Avatar(models.Model):
#     avatar_raw = models.ImageField("User upload avatar", upload_to='upload/%Y%m%d', blank=False, null=False, default="")
#     avatar_l = models.ImageField("large avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")
#     avatar_m = models.ImageField("medium avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")
#     avatar_s = models.ImageField("small avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")

class user_profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile')
    nickname = models.CharField(max_length=256, blank=True, null=True)
    gender = models.IntegerField(null=False, default=-1)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    education = models.CharField(max_length=256, blank=True, null=True)
    tag = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', default='avatar/default.jpg', blank=True, null=True)  # 用户上传图像


class user_behavior(models.Model):
    user = models.ForeignKey(User, related_name='behavior')
    news = models.ForeignKey(news, null=False)
    behavior_type = models.IntegerField(null=False, default=0)
    is_comment = models.BooleanField(default=False)
    is_collect = models.BooleanField(default=False)
    behavior_way = models.IntegerField(null=False, default=1)
    behavior_time = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-behavior_time']


class user_tag_score(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='tag')
    news_entertainment = models.FloatField(default=0, null=False)
    news_fashion = models.FloatField(default=0, null=False)
    news_finance = models.FloatField(default=0, null=False)
    news_game = models.FloatField(default=0, null=False)
    news_sports = models.FloatField(default=0, null=False)
    news_society = models.FloatField(default=0, null=False)
    news_tech = models.FloatField(default=0, null=False)

    # news_car = models.FloatField(default=0,null=False)
    #
    # news_funny = models.FloatField(default=0,null=False)
    # news_military = models.FloatField(default=0,null=False)
    # news_world = models.FloatField(default=0,null=False)
    #
    # news_baby = models.FloatField(default=0,null=False)
    # news_history = models.FloatField(default=0,null=False)
    # news_food = models.FloatField(default=0,null=False)


class user_search(models.Model):
    user = models.ForeignKey(User, related_name='search',null=True)          #有可能没有登陆
    content = models.CharField(max_length=50, null=True)
    key_words = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-date_created']


# 维护一张相似用户矩阵表，离线更新表，避免在线进行大量的计算
class user_similarity(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='similaryity')
    similary_user = models.CharField(null=True, max_length=1000)  # 和user相似的用户，用，隔开
    date_created = models.DateTimeField(auto_now_add=True)  # 更新的时间


# 保存推荐给用户资讯，避免重复推荐
class user_recommendation(models.Model):
    user = models.ForeignKey(User, related_name='recommendation')
    news = models.ForeignKey(news, null=False)  # 推荐过的新闻id
    date_created = models.DateTimeField(auto_now_add=True)  # 推荐的时间

    class Meta():
        ordering = ['-date_created']

#保存给用户推荐的资讯，基于用户协同过滤算法，用于离线计算推荐资讯
class user_cf_recommendation(models.Model):
    user = models.ForeignKey(User,related_name='UserCF')
    news = models.ForeignKey(news,null=False)
    classification = models.CharField(max_length=20)           #分类
    pubtime = models.DateTimeField(auto_now_add=False)         #资讯发布的时间
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-pubtime']



class user_collection(models.Model):
    user = models.ForeignKey(User, related_name='collection')
    news = models.ForeignKey(news, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
