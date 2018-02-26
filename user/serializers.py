# -*- coding: utf-8 -*-
# @Time    : 2018/2/26 14:34
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

from django.contrib.auth.models import User
from rest_framework import serializers
from news.models import news

# class UserSerializer(serializers.ModelSerializer):
#     news = serializers.PrimaryKeyRelatedField(many=True, queryset=news.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'news')