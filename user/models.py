# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 13:56
# @Author  : 陈强
# @FileName: models.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import User
from news.models import news

class Avatar(models.Model):
    avatar_raw = models.ImageField("User upload avatar", upload_to='upload/%Y%m%d', blank=False, null=False, default="")
    avatar_l = models.ImageField("large avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")
    avatar_m = models.ImageField("medium avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")
    avatar_s = models.ImageField("small avatar", upload_to='avatar/%Y%m%d', blank=False, null=False, default="")

class user_profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile')
    nickname = models.CharField(max_length=256, blank=True, null=True)
    gender = models.IntegerField(null=False,default=-1)
    birthday = models.DateField(null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    education = models.CharField(max_length=256, blank=True, null=True)
    tag = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.PROTECT, blank=True, null=True)


class user_behavior(models.Model):
    user = models.ForeignKey(User,related_name='behavior')
    news = models.ForeignKey(news,null=False)
    behavior_type = models.IntegerField(null=False,default=0)
    is_comment = models.BooleanField(default=False)
    is_collect = models.BooleanField(default=False)
    behavior_way = models.IntegerField(null=False,default=1)
    behavior_time = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-behavior_time']

class user_tag(models.Model):
    user = models.OneToOneField(User, primary_key=True,related_name='tag')
    news_society = models.FloatField(default=0,null=False)
    news_tech = models.FloatField(default=0,null=False)
    news_entertainment = models.FloatField(default=0,null=False)
    news_game = models.FloatField(default=0,null=False)
    news_sports = models.FloatField(default=0,null=False)
    news_car = models.FloatField(default=0,null=False)
    news_finance = models.FloatField(default=0,null=False)
    news_funny = models.FloatField(default=0,null=False)
    news_military = models.FloatField(default=0,null=False)
    news_world = models.FloatField(default=0,null=False)
    news_fashion = models.FloatField(default=0,null=False)
    news_baby = models.FloatField(default=0,null=False)
    news_history = models.FloatField(default=0,null=False)
    news_food = models.FloatField(default=0,null=False)

class user_search(models.Model):
    user = models.ForeignKey(User,related_name='search')
    content = models.CharField(max_length=50,null=False)
    keyword = models.CharField(max_length=50,null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-date_created']


