# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 16:15
# @Author  : 陈强
# @FileName: urls.py
# @Software: PyCharm

from rest_framework import routers
from .api import NewsViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
