# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 16:25
# @Author  : 陈强
# @FileName: NaiveBayesPredict.py
# @Software: PyCharm

import pymysql
from sklearn.externals import joblib
import pickle
import jieba
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from news.models import news,news_tag_score


def get_data_dict():

    # conn =pymysql.connect(host='127.0.0.1',user='root',password='1345285903',db='newsrecommendation',charset="utf8")
    # cur = conn.cursor()
    # #取出没有预测过的新闻
    # sql = 'select news_id,content from news_news where is_predict=0'
    # cur.execute(sql)
    # datas = cur.fetchall()
    # cur.close()
    # conn.close()

    datas = news.objects.filter(is_predict=0).values_list()

    data_dict = {}
    for data in datas:
        try:
            data_dict[data[0]] = jieba.lcut(data[6],cut_all=False)
        except:
            print('error',data)
    return data_dict

def update_data(dic):

    news_tag_score.objects.create(**dic)

    news.objects.filter(news_id=dic['news_id']).update(is_predict=1)


def TextFeatures(data_dict,feature_words):
    def text_features(text, feature_words):  # 出现在特征集中，则置1
        text_words = set(text)
        features = [1 if word in text_words else 0 for word in feature_words]
        return features

    feature_dict = {}
    for data in data_dict:
        feature_dict[data] = text_features(data_dict[data], feature_words)

    # feature_list = [text_features(text, feature_words) for text in data_list]
    # test_feature_list = [text_features(text, feature_words) for text in test_data_list]
    return feature_dict # 返回结果

def NBpredict():
    clf = joblib.load('./trainModel/trainModel.m')
    f = open('./trainModel/feature_words.m','rb')
    feature_word = pickle.load(f)
    f.close()
    data_dict = get_data_dict()
    feature_dict = TextFeatures(data_dict,feature_word)

    #对资讯进行预测并更新到数据库中
    for k,v in feature_dict.items():
        proba = clf.predict_proba([v])[0]
        dic = {'news_id':k,'news_entertainment':proba[0],'news_fashion':proba[1],'news_finance':proba[2],'news_game':proba[3],'news_society':proba[4],'news_sports':proba[5],'news_tech':proba[6]}
        update_data(dic)

    # p = clf.predict_proba([feature_dict[42]])
    # print(p)

    # for i in feature_dict:


if __name__=='__main__':
    NBpredict()
