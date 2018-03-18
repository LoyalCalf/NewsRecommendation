# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 11:53
# @Author  : 陈强
# @FileName: NB.py
# @Software: PyCharm

from sklearn.naive_bayes import MultinomialNB
import pickle
import os
import jieba
from sklearn.externals import joblib

"""
函数说明:中文文本处理

Parameters:
	folder_path - 文本存放的路径
Returns:
	all_words_list - 按词频降序排序的训练集列表
	data_list - 训练集列表
	class_list - 训练集标签列表

"""


def trainTextProcessing(folder_path):
    folder_list = os.listdir(folder_path)  # 查看folder_path下的文件
    data_list = []  # 数据集数据
    class_list = []  # 数据集类别

    # 遍历每个子文件夹
    for folder in folder_list:
        new_folder_path = os.path.join(folder_path, folder)  # 根据子文件夹，生成新的路径
        files = os.listdir(new_folder_path)  # 存放子文件夹下的txt文件的列表

        # 遍历每个txt文件
        for file in files:
            with open(os.path.join(new_folder_path, file), 'r', encoding='utf-8') as f:  # 打开txt文件
                raw = f.read()

            word_cut = jieba.cut(raw, cut_all=False)  # 精简模式，返回一个可迭代的generator
            word_list = list(word_cut)  # generator转换为list

            data_list.append(word_list)  # 添加数据集数据
            class_list.append(folder)  # 添加数据集类别

    all_words_dict = {}  # 统计训练集词频
    for word_list in data_list:
        for word in word_list:
            if word in all_words_dict.keys():
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1

    # 根据键的值倒序排序
    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f: f[1], reverse=True)
    all_words_list, all_words_nums = zip(*all_words_tuple_list)  # 解压缩
    all_words_list = list(all_words_list)  # 转换成列表
    return all_words_list, data_list, class_list


"""
函数说明:读取文件里的内容，并去重

Parameters:
	words_file - 文件路径
Returns:
	words_set - 读取的内容的set集合

"""


def MakeWordsSet(words_file):
    words_set = set()  # 创建set集合
    with open(words_file, 'r', encoding='utf-8') as f:  # 打开文件
        for line in f.readlines():  # 一行一行读取
            word = line.strip()  # 去回车
            if len(word) > 0:  # 有文本，则添加到words_set中
                words_set.add(word)
    return words_set  # 返回处理结果


"""
函数说明:根据feature_words将文本向量化

Parameters:
	data_list - 训练集
	feature_words - 特征集
Returns:
	train_feature_list - 训练集向量化列表
"""


def TextFeatures(data_list, feature_words):
    def text_features(text, feature_words):  # 出现在特征集中，则置1
        text_words = set(text)
        features = [1 if word in text_words else 0 for word in feature_words]
        return features

    feature_list = [text_features(text, feature_words) for text in data_list]
    # test_feature_list = [text_features(text, feature_words) for text in test_data_list]
    return feature_list  # 返回结果


"""
函数说明:文本特征选取

Parameters:
	all_words_list - 训练集所有文本列表
	stopwords_set - 指定的结束语
Returns:
	feature_words - 特征集

"""


def words_dict(all_words_list, stopwords_set=set()):
    feature_words = []  # 特征列表
    n = 1
    for t in range(0, len(all_words_list), 1):
        if n > 5000:  # feature_words的维度为5000
            break
        # 如果这个词不是数字，并且不是指定的结束语，并且单词长度大于1小于5，那么这个词就可以作为特征词
        if not all_words_list[t].isdigit() and all_words_list[t] not in stopwords_set and 1 < len(
                all_words_list[t]) < 5:
            feature_words.append(all_words_list[t])
        n += 1
    return feature_words


"""
函数说明:训练模型并保存

Parameters:
	train_feature_list - 训练集向量化的特征文本
	train_class_list - 训练集分类标签
	
"""


def trainTextClassifier(train_feature_list, train_class_list, feature_words):
    classifier = MultinomialNB(alpha=0.1).fit(train_feature_list, train_class_list)
    # s = pickle.dumps(classifier)
    # 保存训练模型
    joblib.dump(classifier, './trainModel/trainModel.m')
    # 保存特征集
    fw = pickle.dumps(feature_words)
    with open('./trainModel/feature_words.m', 'wb') as f:
        f.write(fw)


if __name__ == '__main__':
    # 文本预处理
    folder_path = './trainData'  # 训练集存放地址
    all_words_list, train_data_list, train_class_list = trainTextProcessing(folder_path)

    # 生成stopwords_set
    stopwords_file = 'stop_words.txt'
    stopwords_set = MakeWordsSet(stopwords_file)

    feature_words = words_dict(all_words_list, stopwords_set)

    train_feature_list = TextFeatures(train_data_list, feature_words)

    trainTextClassifier(train_feature_list, train_class_list, feature_words)
