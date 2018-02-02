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

    class Meta():
        ordering = ['-pubtime']

class news_tag_score(models.Model):
    news = models.OneToOneField(news,on_delete=models.CASCADE,primary_key=True)
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

class news_comment(models.Model):
    content = models.TextField(null=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='comment_user')
    news = models.ForeignKey(news,on_delete=models.CASCADE)
    parent_user = models.ForeignKey(User,on_delete=models.PROTECT,null=True,related_name='reply_user')
    root_user = models.ForeignKey(User,on_delete=models.PROTECT,null=True,related_name='root_user')

    class Meta():
        ordering = ['-comment_time']

class news_profile(models.Model):
    news = models.OneToOneField(news,on_delete=models.CASCADE,primary_key=True)
    viewed_count = models.IntegerField(null=False,default=0)
    comment_count = models.IntegerField(null=False,default=0)
    liked_count = models.IntegerField(null=False,default=0)
    dislike_count = models.IntegerField(null=False,default=0)
    collected_count = models.IntegerField(null=False,default=0)