# -*- coding: utf-8 -*-
# @Time    : 2018/2/26 14:34
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

from django.contrib.auth.models import User
from rest_framework import serializers
from news.models import news
from user.models import user_profile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_profile
        fields = '_all_'