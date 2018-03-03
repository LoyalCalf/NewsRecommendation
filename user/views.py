# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 15:56
# @Author  : 陈强
# @FileName: views.py
# @Software: PyCharm

from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets, renderers

from rest_framework.response import Response
from user.models import user_behavior
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics

class Login(APIView):
    """
    登陆api，post请求，需要username和password参数（暂时的要求）
    """

    def post(self,request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return Response({'msg':'登陆成功','code':200})
            else:
                return Response({'msg':'用户名或密码错误','code':300})
        except:
            return Response({'msg': '参数错误', 'code': 300})

class Register(APIView):
    """
    注册API
    """
    def post(self,request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = auth.authenticate(username=username, password=password)
            if user:
                return Response({'msg':'用户已存在','code':300})
            User.objects.create_user(username=username,password=password,email=email)
            # user.save()
            return Response({'msg':'注册成功','code':200})
        except:
            return Response({'msg':'参数错误','code':300})



class UserBehavior(APIView):
    """
    用户的行为API，比如浏览一条新闻，点赞，不喜欢等行为
    """

    # @method_decorator(csrf_exempt)
    def get(self,request):

        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            # print(request.POST)
            try:
                behavior_type = request.GET['behavior_type']
                news_id = request.GET['news_id']
            except:
                return Response({'msg':'参数错误','code':300})

            dic = {'behavior_type':behavior_type,'news_id':news_id,'user_id':user.id}
            user_behavior.objects.create(**dic)
            res = {'msg':'success','code':200}
            return Response(res)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)