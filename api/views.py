# -*- coding: utf-8 -*-
# @Time    : 2018/3/18 14:20
# @Author  : 陈强
# @FileName: views.py
# @Software: PyCharm


from api.serializers import NewsAbstractSerializer, NewsContentSerializer, NewsCommentSerializer
from news.models import news, news_profile, news_hot, news_comment, search_hot
from rest_framework import generics
from algorithm.Recommendation import UserCF, ContentBased
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from user.utils import create_thumbnail, Token
from rest_framework.response import Response
from user.models import user_behavior, user_profile, user_tag_score, user_search, user_collection
from rest_framework.views import APIView
from algorithm.Recommendation.genUserTag import UserTag
from datetime import datetime, timedelta


"""News"""


# class NewsList(generics.ListCreateAPIView):
#     """
#     请求：GET
#     功能：所有新闻的API
#     参数：offset和limit
#     URL格式：api/news/(news_id)
#     例子：api/news/?limit=10&offset=10
#     说明：带上news_id则请求具体的新闻内容
#     """
#     queryset = news.objects.all()
#     serializer_class = NewsAbstractSerializer

class NewsList(APIView):
    """
    请求：GET
    功能：所有新闻的API
    参数：offset和limit
    URL格式：api/news/(news_id)
    例子：api/news/?limit=10&offset=10
    说明：带上news_id则请求具体的新闻内容
    """

    def get(self, request):
        classification = request.GET.get('classification')
        offset = int(request.GET.get('offset', 0))
        limit = 10
        if classification:
            news_list = news.objects.filter(classification=classification).order_by('-pubtime')[offset:offset + limit]
        else:
            news_list = news.objects.order_by('-pubtime')[offset:offset + limit]
        serializer = NewsAbstractSerializer(news_list, many=True)
        return Response({'code': 200, 'msg': 'success', 'results': serializer.data})


class NewsContent(generics.RetrieveUpdateDestroyAPIView):
    queryset = news.objects.all()
    serializer_class = NewsContentSerializer


class CBRecommendation(APIView):
    """
    请求：GET
    功能：基于内容的资讯推荐
    参数：classification（类型，直接使用中文，比如classification=社会，也可以不传递，则返回所有类型的推荐），offset
    URL格式：api/news_recommendation/?classification=社会&offset=10
    说明：offset主要是为了给未登陆用户推荐热点新闻，如果用户登录则推荐新闻，该参数没有影响，因此统一传递此参数
    """

    def get(self, request):
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            classification = request.GET.get('classification', None)

            news_read = user_behavior.objects.filter(user_id=user.id, behavior_type__in=[1, 2]).order_by(
                '-behavior_time')[:1]
            if news_read.exists():
                news_id = news_read[0].news_id
            else:
                hot = news_hot.objects.order_by('-pubtime')[:1]  # 用户没有浏览过资讯就已最新的热点新闻作为基础
                news_id = hot[0].news_id

            recom_news_id = ContentBased.ContentBasedRecommendation().recommendation(user.id, news_id, classification)
            newsList = news.objects.filter(news_id__in=recom_news_id)
            serializer = NewsAbstractSerializer(newsList, many=True)
            return Response({'code': 200, 'msg': 'success', 'results': serializer.data})

            # newsID = UserCF.UserCF_Recommendation().get_data(user.id)
            # if not newsID:
            #     return Response({'msg':'暂时没有该用户的推荐结果','code':300})
            # newsList = news.objects.filter(news_id__in=newsID)
            # serializer = NewsAbstractSerializer(newsList, many=True)
            # return Response(serializer.data)

        else:
            classification = request.GET.get('classification', '')
            offset = int(request.GET.get('offset', 0))
            limit = 10
            if classification:
                news_id_list = list(news_hot.objects.filter(classification=classification).order_by('score')[
                                    offset:offset + limit].values_list('news_id', flat=True))
            else:
                news_id_list = list(news_hot.objects.all()[offset:offset + limit].values_list('news_id', flat=True))
            news_list = news.objects.filter(news_id__in=news_id_list)
            serializer = NewsAbstractSerializer(news_list, many=True)
            return Response({'code': 200, 'msg': 'success', 'results': serializer.data})
            # res = {'msg':'用户未登陆','code':300}
            # return Response(res)


class UserCFRecommendation(APIView):
    """
    请求：GET
    功能：上拉时资讯推荐，基于用户的协同过滤算法，
    参数：classification（类型，直接使用中文，比如classification=社会，也可以不传递，则返回所有类型的推荐），offset
    URL格式：api/news_recommendation/?classification=社会&offset=10
    说明：offset主要是为了给未登陆用户推荐热点新闻，如果用户登录则推荐新闻，该参数没有影响，因此统一传递此参数
    """

    def get(self, request):
        pass


class NewsComments(APIView):
    """
    请求：GET或POST
    功能：资讯评论
    """

    def get(self, request):
        """
        获取评论
        :param request:news_id,offset
        :return:
        """
        try:
            news_id = request.GET.get('news_id')
            offset = request.GET.get('offset', 0)
            limit = 10
            root_comment = news_comment.objects.filter(news_id=news_id, root_id=-1).order_by('-comment_time')[
                           offset:offset + limit]  # 取出根评论
            serializer = NewsCommentSerializer(root_comment, many=True)
            return Response(serializer.data)

        except:
            pass
        return Response({'msg': 'error', 'code': 300})

    def post(self, request):
        """
        用户评论
        :param request:content(用户评论内容)，news_id（被评论的资讯）
        :return:
        """
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            user_id = user.id
            try:
                content = request.POST.get('content', '')
                news_id = request.POST.get('news_id')
                if not news_id:
                    return Response({'msg': '参数错误', 'code': 300})
                root_id = request.POST.get('root_id', -1)
                parent_user_id = request.POST.get('parent_user_id')
                # if parent_user_id:
                news_comment.objects.create(content=content, news_id=news_id, root_id=root_id,
                                            parent_user_id=parent_user_id, user_id=user_id)
                # else:
                #     news_comment.objects.create(content=content, news_id=news_id, root_id=root_id, user_id=user_id)
                return Response({'msg': 'success', 'code': 200})
            except:
                return Response({'msg': '参数错误', 'code': 300})


        else:
            res = {'msg': '用户未登陆', 'code': 300}
            return Response(res)


"""热点新闻"""


class NewsHot(APIView):
    def get(self, request):
        try:
            classification = request.GET.get('classification', '')
            offset = int(request.GET.get('offset', 0))
            limit = 10
            if classification:
                news_id_list = list(news_hot.objects.filter(classification=classification).order_by('score')[
                                    offset:offset + limit].values_list('news_id', flat=True))
            else:
                news_id_list = list(news_hot.objects.all()[offset:offset + limit].values_list('news_id', flat=True))
            news_list = news.objects.filter(news_id__in=news_id_list)
            serializer = NewsAbstractSerializer(news_list, many=True)
            return Response(serializer.data)
        except:

            return Response({'msg': 'error', 'code': 300})


"""用户搜索"""


class NewsSearch(APIView):
    """
    请求：GET
    功能：用户搜索后将搜索的内容发给后台
    参数：q(搜索内容)
    """

    def get(self, request):
        if request.user.is_authenticated():
            user_id = User.objects.get(username=request.user.username).id
        else:
            user_id = None
        q = request.GET.get('q')
        if not q:
            return Response({'msg': 'error', 'code': 300})
        dic = {'content': q, 'key_words': q, 'user_id': user_id}
        user_search.objects.create(**dic)
        return Response({'msg': 'success', 'code': 200})


"""热搜"""


class HotSearch(APIView):
    """
    请求：GET
    功能：返回热搜
    参数：_t(时间戳),hours(多长时间内的热搜，比如24小时热搜)
    格式：api/hot_search/?_t=15xxxxxxxxxx&hours=24
    """

    def get(self, request):
        _t = request.GET.get('_t')
        hours = request.GET.get('hours', 24)
        min_time = self._get_days_before_today(hours)
        res = search_hot.objects.filter(date_created__gte=min_time).order_by('-count')[:10]
        data = [i.key_words for i in res]
        return Response({'results': data})

    def _get_days_before_today(self, hours):
        return datetime.now() - timedelta(hours=hours)


"""User"""

"""登陆"""


class Login(APIView):
    """
    请求：POST
    功能：用户登录API
    参数：username，password（暂时两个参数）
    """

    def post(self, request):

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            # print(make_password(password))
            # user = User.objects.get(username=username)

            # print(user)
            # if check_password(password,user.password):
            if user:
                auth.login(request, user)
                return Response({'msg': '登陆成功', 'code': 200})
            else:
                return Response({'msg': '密码错误', 'code': 300})
        except:
            return Response({'msg': '用户不存在', 'code': 300})


"""注销"""


class Logout(APIView):
    """
    请求：POST
    功能：用户注销

    """

    def post(self, request):
        if request.user.is_authenticated():
            auth.logout(request)
            return Response({'msg': 'success', 'code': 200})
        else:
            return Response({'msg': 'error', 'code': 300})


"""注册"""


class Register(APIView):
    """
    请求：POST
    功能：用户注册API
    参数：username，password，email
    """

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = User.objects.filter(username=username)

            # 暂时允许邮箱重复，便于测试

            if user.exists():
                return Response({'msg': '用户已存在', 'code': 300})
            user = User.objects.create_user(username=username, password=password, email=email, is_active=True)
            # User.objects.create_user(username=username,password=password,email=email,is_active=False)
            # self._send_register_email(user)
            # user.save()
            user_profile.objects.create(user_id=user.id, nickname=username)  # 注册完成同时添加额外信息，保证信息完整
            user_tag_score.objects.create(user_id=user.id)
            # user.save()
            return Response({'msg': '注册成功,请尽快完成邮箱验证', 'code': 200})
        except:
            return Response({'msg': '错误', 'code': 300})

    def _send_register_email(self, user):
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


"""用户行为信息"""


class UserBehavior(APIView):
    """
    请求：GET
    功能：用户的行为API，比如浏览一条新闻，点赞，不喜欢等行为
    参数：behavior_type（具体参数参看数据库建模文档），news_id（对某条资讯产生的行为）,behavoir_way(产生行为的方式，搜索阅读和推荐阅读)
    """

    def get(self, request):

        if request.user.is_authenticated():
            user = User.objects.get(username=request.user.username)
            # print(request.POST)
            behavior_type = int(request.GET.get('behavior_type', 1))
            behavior_way = int(request.GET.get('behavior_way', 1))
            news_id = int(request.GET.get('news_id'))
            dic = {'behavior_type': behavior_type, 'news_id': news_id, 'user_id': user.id, 'behavior_way': behavior_way}
            user_behavior.objects.create(**dic)
            UserTag(news_id, user.id, behavior_type, behavior_way).calculate()  # 更新用户兴趣表
            res = {'msg': 'success', 'code': 200}
            return Response(res)
        else:
            res = {'msg': '用户未登陆', 'code': 300}
            return Response(res)


"""用户信息设置"""


class UserProfileSetting(APIView):
    """
    请求：POST
    功能：用户资料设置
    参数：参看数据库说明文档
    """

    def post(self, request):
        if request.user.is_authenticated():
            nickname = request.POST.get('nickname', request.user.username)
            gender = int(request.POST.get('gender', -1))
            birthday = request.POST.get('birthday')
            location = request.POST.get('location')
            education = request.POST.get('education')
            tag = request.POST.get('tag')
            description = request.POST.get('description')
            avatar = request.FILES.get('avatar')
            dic = {'user_id': request.user.id, 'nickname': nickname, 'gender': gender, 'birthday': birthday,
                   'location': location, 'education': education, 'tag': tag, 'description': description}

            if avatar:
                new_name = get_random_string(length=6)
                ext = str(avatar).split('.')[-1]
                avatar_name = '%s.%s' % (new_name, ext)
                large = create_thumbnail(avatar, new_name, ext)
                # SimpleUploadedFile(avatar_name,img)
                dic['avatar'] = large

            user_profile.objects.update_or_create(**dic)
            return Response({'msg': '修改信息成功', 'code': 200})

        else:
            res = {'msg': '用户未登陆', 'code': 300}
            return Response(res)


"""用户收藏资讯"""


class UserCollection(APIView):
    def get(self, request):
        """
        请求：GET
        功能：获取用户收藏的资讯
        参数：offset(每次取10条，offset表示偏移量)
        URL：api/user_collection/?offset=10
        """
        if request.user.is_authenticated():
            offset = int(request.GET.get('offset', 0))
            limit = 10
            user_id = User.objects.get(username=request.user.username).id
            news_list = user_collection.objects.filter(user_id=user_id).order_by('-date_created')[offset:offset + limit]
            results = []
            for i in news_list:
                news_info = news.objects.get(news_id=i.news_id)
                results.append(
                    {'id': news_info.id, 'title': news_info.title, 'date': i.date_created, 'image': news_info.image})
            return Response({'msg': 'success', 'code': 200, 'results': results})
        else:
            return Response({'msg': '用户未登陆', 'code': 300})

    def post(self, request):
        """
        请求：POST
        功能：用户点击收藏后将信息发送给后台
        参数：news_id(表示要收藏的资讯id)
        """
        if request.user.is_authenticated():
            user_id = User.objects.get(username=request.user.username).id
            news_id = request.POST.get('news_id')
            user_collection.objects.create(user_id=user_id, news_id=news_id)
            return Response({'msg': 'success', 'code': 200})
        else:
            return Response({'msg': '用户未登陆', 'code': 300})

# 用户邮箱验证
# class active_user(TemplateView):
#     def get(self, request, *args, **kwargs):
#
#         # def active_user(request, token):
#         token_confirm = Token(settings.SECRET_KEY)
#         try:
#             username = token_confirm.confirm_validate_token(kwargs['token'])
#         except:
#             return HttpResponse('对不起，验证链接已经过期')
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return HttpResponse('对不起，您所验证的用户不存在，请重新注册')
#         user.is_active = True
#         user.save()
#         return render(request, 'index.html')
