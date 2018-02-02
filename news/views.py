# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: serializers.py
# @Software: PyCharm

from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, renderers

from rest_framework.response import Response
from .serializers import NewsSerializer
from .models import news
from django.shortcuts import render

def index(request):
    return render(request,'index.html')
