# -*-coding:utf-8-*-
__author__ = '陈强'

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class news(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_link = models.CharField(max_length=255,blank=True,null=True,unique=True)
    source = models.CharField(max_length=255,blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    pubtime = models.DateTimeField(blank=True,null=True)
    abstract = models.TextField(blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    html_content = models.TextField(blank=True,null=True)
    # editor = models.CharField(max_length=255,blank=True,null=True)
    image = models.CharField(max_length=1000,blank=True,null=True)
    tag = models.CharField(max_length=1000,blank=True,null=True)
    classification = models.CharField(max_length=20,blank=True,null=True)   #爬取新闻的分类
    is_predict = models.BooleanField(default=False)                  #是否预测过其分类

    class Meta():
        ordering = ['-pubtime']

class news_tag_score(models.Model):
    news = models.OneToOneField(news,on_delete=models.CASCADE,primary_key=True)

    news_entertainment = models.FloatField(default=0,null=False)
    news_fashion = models.FloatField(default=0, null=False)
    news_finance = models.FloatField(default=0, null=False)
    news_game = models.FloatField(default=0, null=False)
    news_sports = models.FloatField(default=0, null=False)
    news_society = models.FloatField(default=0,null=False)
    news_tech = models.FloatField(default=0,null=False)

    # news_car = models.FloatField(default=0,null=False)
    #
    # news_funny = models.FloatField(default=0,null=False)
    # news_military = models.FloatField(default=0,null=False)
    # news_world = models.FloatField(default=0,null=False)
    #
    # news_baby = models.FloatField(default=0,null=False)
    # news_history = models.FloatField(default=0,null=False)
    # news_food = models.FloatField(default=0,null=False)

class news_comment(models.Model):
    #id:自增id

    content = models.TextField(null=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='user_comment')     #评论的用户
    news = models.ForeignKey(news,on_delete=models.CASCADE,related_name='comment')
    parent_user = models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True,related_name='reply_user')      #是否回复某人
    root_id = models.IntegerField(default=-1)         #根评论，某条评论下是否还有评论
    reply_count = models.IntegerField(default=0)      #某条评论下回复的数量，默认为0

    class Meta():
        ordering = ['-comment_time']

class news_profile(models.Model):
    news = models.OneToOneField(news,on_delete=models.CASCADE,primary_key=True,related_name='news_profile')
    viewed_count = models.IntegerField(null=False,default=0)
    comment_count = models.IntegerField(null=False,default=0)
    liked_count = models.IntegerField(null=False,default=0)
    dislike_count = models.IntegerField(null=False,default=0)
    collected_count = models.IntegerField(null=False,default=0)
    pubtime = models.DateTimeField(blank=True,null=True)
    # class Meta():
    #     ordering = ['-viewed_count','liked_count']

class news_hot(models.Model):
    """
    热点新闻纪录，纪录哪些新闻曾
    """
    news = models.OneToOneField(news,on_delete=models.CASCADE,primary_key=True)
    score = models.FloatField(default=0)
    pubtime = models.DateTimeField(blank=True, null=True)   #新闻发布时间
    date_created = models.DateTimeField(auto_now_add=True)   #成为热点新闻的时间
    classification = models.CharField(max_length=20,blank=True, null=True)
    class Meta():
        ordering = ['-score','-pubtime']
