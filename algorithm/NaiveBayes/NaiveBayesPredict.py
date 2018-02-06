# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 16:25
# @Author  : 陈强
# @FileName: NaiveBayesPredict.py
# @Software: PyCharm

import pymysql
from sklearn.externals import joblib
import pickle
import jieba
from sklearn.naive_bayes import MultinomialNB


# def get_data():
#     conn =pymysql.connect(host='127.0.0.1',user='root',password='1345285903',db='newsrecommendation',charset="utf8")
#     cur = conn.cursor()
#     sql = 'select news_id,content from news_news where is_predict=0'
#     cur.execute(sql)
#     data = cur.fetchall()
#     return data

def get_data_dict():

    conn =pymysql.connect(host='127.0.0.1',user='root',password='1345285903',db='newsrecommendation',charset="utf8")
    cur = conn.cursor()
    #取出没有预测过的新闻
    sql = 'select news_id,content from news_news where is_predict=0'
    cur.execute(sql)
    datas = cur.fetchall()
    cur.close()
    conn.close()

    data_dict = {}
    for data in datas:
        try:
            data_dict[data[0]] = jieba.lcut(data[1],cut_all=False)
        except:
            print('error',data)
    return data_dict


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
    data_dict = get_data_dict()
    feature_dict = TextFeatures(data_dict,feature_word)

    p = clf.predict_proba([feature_dict[42]])
    print(p)

    # for i in feature_dict:


if __name__=='__main__':
    NBpredict()
