# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 10:55
# @Author  : 陈强
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url, include
from user import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^user_info/', views.user_info),
    url(r'^user_change/', views.user_change),

    url(r'^account/activate/(?P<token>[\w\-]+.[\w\-]+.[\w\-]+)/$', views.active_user.as_view(), name='active_user')
]
