# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 15:56
# @Author  : 陈强
# @FileName: views.py
# @Software: PyCharm

from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, renderers

from rest_framework.response import Response
from .serializers import NewsAbstractSerializer,NewsContentSerializer
from .models import news
from user.models import user_behavior
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from algorithm.Recommendation import UserCF,ContentBased


def index(request):
    return render(request,'index.html')


class NewsList(generics.ListCreateAPIView):
    """
    所有新闻的API
    """
    queryset = news.objects.all()
    serializer_class = NewsAbstractSerializer

class NewsContent(generics.RetrieveUpdateDestroyAPIView):
    queryset = news.objects.all()
    serializer_class = NewsContentSerializer

class NewsRecommendation(APIView):
    """
    所有类型推荐新闻api
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            newsID = UserCF.UserCF_Recommendation().get_data(user.id)
            newsList = news.objects.filter(news_id__in=newsID)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)


class NewsRecommendationSociety(APIView):
    """
    社会类型资讯推荐
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'社会')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class NewsRecommendationGame(APIView):
    """
    游戏类型资讯推荐
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'游戏')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class NewsRecommendationEntertainment(APIView):
    """
    娱乐类型资讯推荐
    """

    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'娱乐')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class NewsRecommendationSports(APIView):
    """
    体育类型资讯推荐
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'体育')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class NewsRecommendationFinance(APIView):
    """
    财经类型资讯推荐
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'财经')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class NewsRecommendationFashion(APIView):
    """
    时尚类型资讯推荐
    """
    def get(self,request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            news_read = user_behavior.objects.filter(user_id=user.id,behavior_type__in=[1,2]).order_by('-behavior_time')[:1]

            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                news_id = 1
            recom_news_id = ContentBased.ContentBasedRecommendation(user.id,news_id,'时尚')
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response(serializer.data)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)


class NewsComments(APIView):
    """
    资讯评论
    """

    def get(self,request):
        """
        获取评论
        :param request:
        :return:
        """

        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)

        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)
        pass

    def post(self,request):
        """
        用户评论
        :param request:
        :return:
        """
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            user_id = user.id
            try:
                content = request.POST['content']
                news_id = request.POST['news_id']

            except:
                return Response({'msg': '参数错误', 'code': 300})


        else:
            res = {'msg': '用户未登陆', 'code': 300}
            return Response(res)
