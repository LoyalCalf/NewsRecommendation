# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 18:33
# @Author  : 陈强
# @FileName: api.py
# @Software: PyCharm

from rest_framework import permissions, viewsets, renderers

from rest_framework.response import Response
from .serializers import NewsSerializer
from .models import news


class NewsViewSet(viewsets.ModelViewSet):
    queryset = news.objects.all()
    serializer_class = NewsSerializer