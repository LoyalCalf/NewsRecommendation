# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

from __future__ import unicode_literals, absolute_import
import json

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import news,news_profile

class NewsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = news_profile
        fields = ('viewed_count', 'comment_count')

class NewsSerializer(serializers.ModelSerializer):
    # newsProfile = NewsProfileSerializer()
    class Meta:
        model = news
        fields = ('news_id', 'news_link', 'source', 'title', 'abstract','tag','classification')

