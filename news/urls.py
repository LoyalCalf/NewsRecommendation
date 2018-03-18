# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 16:15
# @Author  : 陈强
# @FileName: urls.py
# @Software: PyCharm

from rest_framework import routers
# from .api import NewsViewSet,ContentBaseRecommendationNews
#
# router = routers.DefaultRouter()
# router.register(r'news', NewsViewSet)
# router.register(r'recom',ContentBaseRecommendationNews)

from django.conf.urls import url, include
from news import views

urlpatterns = [

    url(r'^$',views.index),

    url(r'^news/(?P<news_id>[0-9]+)/$', views.news_content),

    # url(r'^news/$', api.NewsList.as_view()),
    # url(r'^news/(?P<pk>[0-9]+)/$', api.NewsContent.as_view()),
    # url(r'^news_recommendation/', api.NewsRecommendation.as_view()),
    # # url(r'^news_society/', views.NewsRecommendationSociety.as_view()),
    # # url(r'^news_game/', views.NewsRecommendationGame.as_view()),
    # # url(r'^news_entertainment/', views.NewsRecommendationEntertainment.as_view()),
    # # url(r'^news_sports/', views.NewsRecommendationSports.as_view()),
    # # url(r'^news_finance/', views.NewsRecommendationFinance.as_view()),
    # # url(r'^news_fashion/', views.NewsRecommendationFashion.as_view()),
    # url(r'^news_hot/', api.NewsHot.as_view()),
    # url(r'^news_comment/', api.NewsComments.as_view()),
    #
    url(r'^search/', include('haystack.urls')),

]
