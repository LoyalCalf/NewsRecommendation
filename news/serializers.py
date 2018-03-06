# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

import json

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import news,news_comment
from user.models import user_profile



class NewsAbstractSerializer(serializers.ModelSerializer):
    # newsProfile = NewsProfileSerializer()
    class Meta:
        model = news
        fields = ('news_id', 'news_link', 'source', 'pubtime','title', 'abstract','image','classification')

class NewsContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = news
        fields = ('news_id', 'news_link', 'source', 'pubtime', 'title', 'content','html_content', 'image', 'tag', 'classification')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_profile
        fields = ('user_id', 'nickname')

class NewsCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    def get_user(self,obj):
        user = user_profile.objects.filter(user_id=obj)
        return UserProfileSerializer(user,many=True).data

    class Meta:
        model = news_comment
        fields = ('id','content','comment_time','news_id','parent_user_id','user')





# class NewsHotSerializer(serializers.ModelSerializer):
#     news_link = serializers.ReadOnlyField(source='news.news_link')
#     source = serializers.ReadOnlyField(source='news.source')
#     pubtime = serializers.ReadOnlyField(source='news.pubtime')
#     title = serializers.ReadOnlyField(source='news.title')
#     abstract = serializers.ReadOnlyField(source='news.abstract')
#     image = serializers.ReadOnlyField(source='news.image')
#     classification = serializers.ReadOnlyField(source='news.classification')
#
#
#     class Meta:
#         model = news_hot
#         fields = ('news_id','news_link','source','pubtime','title','abstract','image','classification')
