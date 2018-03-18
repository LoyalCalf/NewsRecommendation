# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 13:10
# @Author  : 陈强
# @FileName: LatentFactor.py
# @Software: PyCharm

"""
潜在因子算法，利用用户-兴趣矩阵和资讯-标签分数矩阵
"""


class LatentFactor(object):
    def __init__(self):
        # 用户标签矩阵
        self.user_tag = []
        # 资讯标签矩阵
        self.news_tag = []
