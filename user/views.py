# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 15:56
# @Author  : 陈强
# @FileName: views.py
# @Software: PyCharm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from user.utils import create_thumbnail,Token
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from user.models import user_behavior,user_profile,user_tag_score
from django.shortcuts import render
from rest_framework.views import APIView
from algorithm.Recommendation.genUserTag import UserTag

class Login(APIView):
    """
    请求：POST
    功能：用户登录API
    参数：username，password（暂时两个参数）
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
    请求：POST
    功能：用户注册API
    参数：username，password，email
    """
    def post(self,request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = User.objects.filter(username=username)

            #暂时允许邮箱重复，便于测试

            if user.exists():
                return Response({'msg':'用户已存在','code':300})
            user = User(username=username,password=make_password(password),email=email,is_active=False)
            # User.objects.create_user(username=username,password=password,email=email,is_active=False)
            self._send_register_email(user)
            user.save()
            user_profile.objects.create(user_id=user.id,nickname=username) #注册完成同时添加额外信息，保证信息完整
            user_tag_score.objects.create(user_id=user.id)
            # user.save()
            return Response({'msg':'注册成功,请尽快完成邮箱验证','code':200})
        except:
            return Response({'msg':'错误','code':300})

    def _send_register_email(self,user):
        token_confirm = Token(settings.SECRET_KEY)
        token = token_confirm.generate_validate_token(user.username)
        # active_key = base64.encodestring(username)
        # send email to the register email
        message = "\n".join([
            u'{0},欢迎加入'.format(user.username),
            u'请访问该链接，完成用户验证:',
            '/'.join(['http://127.0.0.1:8000', 'account/activate', token])
        ])
        send_mail('注册用户验证信息', message, '1345285903@qq.com', [str(user.email)])



class UserBehavior(APIView):
    """
    请求：GET
    功能：用户的行为API，比如浏览一条新闻，点赞，不喜欢等行为
    参数：behavior_type（具体参数参看数据库建模文档），news_id（对某条资讯产生的行为）,behavoir_way(产生行为的方式，搜索阅读和推荐阅读)
    """

    # @method_decorator(csrf_exempt)
    def get(self,request):

        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            # print(request.POST)
            behavior_type = request.GET.get('behavior_type',1)
            behavior_way = request.GET.get('behavior_way',1)
            news_id = request.GET.get('news_id')
            dic = {'behavior_type':behavior_type,'news_id':news_id,'user_id':user.id,'behavior_way':behavior_way}
            user_behavior.objects.create(**dic)
            UserTag(news_id,user.id,behavior_type,behavior_way).calculate()      #更新用户兴趣表
            res = {'msg':'success','code':200}
            return Response(res)
        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

class UserProfileSetting(APIView):
    """
    请求：POST
    功能：用户资料设置
    参数：参看数据库说明文档
    """

    def post(self,request):
        if request.user.is_authenticated():
            nickname = request.POST.get('nickname',request.user.username)
            gender = request.POST.get('gender',-1)
            birthday = request.POST.get('birthday')
            location = request.POST.get('location')
            education = request.POST.get('enducation')
            tag = request.POST.get('tag')
            description = request.POST.get('description')
            avatar = request.FILES.get('avatar')
            dic = {'user_id':request.user.id,'nickname':nickname,'gender':gender,'birthday':birthday,'location':location,'education':education,'tag':tag,'description':description}

            if avatar:
                new_name = get_random_string(length=6)
                ext = str(avatar).split('.')[-1]
                avatar_name = '%s.%s'%(new_name,ext)
                large = create_thumbnail(avatar,new_name,ext)
                # SimpleUploadedFile(avatar_name,img)
                dic['avatar'] = large

            user_profile.objects.update_or_create(**dic)
            return Response({'msg':'修改信息成功','code':200})

        else:
            res = {'msg':'用户未登陆','code':300}
            return Response(res)

"""用户收藏资讯"""
class UserCollection(APIView):
    pass

#用户邮箱验证
class active_user(TemplateView):

    def get(self, request, *args, **kwargs):

    # def active_user(request, token):
        token_confirm = Token(settings.SECRET_KEY)
        try:
            username = token_confirm.confirm_validate_token(kwargs['token'])
        except:
            return HttpResponse('对不起，验证链接已经过期')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('对不起，您所验证的用户不存在，请重新注册')
        user.is_active = True
        user.save()
        return render(request,'index.html')
