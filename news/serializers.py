# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

import json

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import news,news_profile

# class NewsProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = news_profile
#         fields = ('viewed_count', 'comment_count')

class NewsAbstractSerializer(serializers.ModelSerializer):
    # newsProfile = NewsProfileSerializer()
    class Meta:
        model = news
        fields = ('news_id', 'news_link', 'source', 'pubtime','title', 'abstract','image','classification')

class NewsContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = news
        fields = ('news_id', 'news_link', 'source', 'pubtime', 'title', 'content','html_content', 'image', 'tag', 'classification')


