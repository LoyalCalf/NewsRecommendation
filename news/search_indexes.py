# -*- coding: utf-8 -*-
# @Time    : 2018/2/28 17:03
# @Author  : 陈强
# @FileName: search_indexes.py
# @Software: PyCharm

import datetime
from haystack import indexes
from news.models import news


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # author = indexes.CharField(model_attr='user')
    pubtime = indexes.DateTimeField(model_attr='pubtime')

    def get_model(self):
        return news

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pubtime__lte=datetime.datetime.now()).order_by('-pubtime')
