# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 13:47
# @Author  : 陈强
# @FileName: ContentBased.py
# @Software: PyCharm

"""
基于内容的推荐算法，用做在线推荐，比如用户刚刚浏览了某些资讯，可以计算和这些资讯相似的资讯并推荐
"""
import numpy as np
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from news.models import news_tag_score, news
from user.models import user_recommendation

def get_data(user_id,news_id):

    #可以取出 当天资讯（考虑时间因素），过滤掉已经推荐过给用户的资讯（去重因素）
    news_recommendation = user_recommendation.objects.filter(user_id=user_id)
    news_recommendation_list = []    #推荐过的news_id列表
    for i in news_recommendation:
        news_recommendation_list.append(i.news_id)
    news_recommendation_list.append(news_id)

    news_data = news_tag_score.objects.filter(news_id=news_id).values_list()
    other_news_data = news_tag_score.objects.exclude(news_id__in=news_recommendation_list).values_list()

    return news_data,other_news_data


#更新推荐表
def update_data(user_id,news_id):
    user_recommendation.objects.create(user_id=user_id,news_id=news_id)



#余弦相似度，用于计算两个资讯间的相似度
def cosine_similarity(x,y):
    one = np.array(x)
    two = np.array(y)
    num = sum(np.multiply(one,two))
    denom = np.linalg.norm(x)*np.linalg.norm(y)
    return round(num/float(denom),3)

#根据用户id，资讯id，推荐10条和此资讯最相似的资讯
def ContentBasedRecommendation(user_id,news_id):
    news_data,other_news_data = get_data(user_id,news_id)
    #当前资讯的特征值行向量
    news_matrix = list(news_data[0][1:])
    #取出的资讯特征值字典 如 1:[0.1,0.2....]
    other_news_dict = {}
    #资讯相似度字典
    similarity_dict = {}
    #推荐列表,元素为news_id
    recommendation_list = []

    for i in other_news_data:
        other_news_dict[i[0]] = list(i[1:])

    for k,v in other_news_dict.items():
        similarity_dict[k] = cosine_similarity(news_matrix,v)

    #对分数进行排序
    sorted_list = sorted(similarity_dict.items(),key=lambda item:item[1],reverse=True)

    count = 0
    for k in sorted_list:
        if count>=10:
            break
        recommendation_list.append(k[0])
        update_data(user_id,k[0])
        count += 1

    # print(recommendation_list)
    return recommendation_list

if __name__=='__main__':

    ContentBasedRecommendation(1,1)