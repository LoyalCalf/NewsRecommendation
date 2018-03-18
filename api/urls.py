# -*- coding: utf-8 -*-
# @Time    : 2018/3/18 14:33
# @Author  : 陈强
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^news/$', views.NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)/$', views.NewsContent.as_view()),
    url(r'^news_recommendation/', views.NewsRecommendation.as_view()),
    url(r'^news_hot/', views.NewsHot.as_view()),
    url(r'^news_comment/', views.NewsComments.as_view()),

    url(r'^user_behavior/$', views.UserBehavior.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^register/$', views.Register.as_view()),
    url(r'^user_profile/$', views.UserProfileSetting.as_view()),

    # url(r'^news_search/', include('haystack.urls')),

]
