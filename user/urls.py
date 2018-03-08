# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 10:55
# @Author  : 陈强
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url, include
from user import views

urlpatterns = [

    url(r'^user_behavior/$', views.UserBehavior.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^register/$', views.Register.as_view()),
    url(r'^user_profile/$', views.UserProfileSetting.as_view()),

]