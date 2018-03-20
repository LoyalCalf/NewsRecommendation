# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: views.py
# @Software: PyCharm

from django.shortcuts import render
from haystack.views import SearchView

def index(request):
    return render(request, 'index.html')

def news_content(request,news_id):
    return render(request,'news/concrete_view.html')




