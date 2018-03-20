# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 21:19
# @Author  : 陈强
# @FileName: cache_manager.py
# @Software: PyCharm

"""
缓存管理，暂定用在用户点赞的地方
"""

from django.conf import settings
from django.core.cache import cache



# user1对user2是否点赞
def is_liked(news_id, user1_id, user2_id):
    key = str(news_id) + ':' + str(user1_id) + '_to_' + str(user2_id)
    value = cache.get(key)
    if value == 1:
        return True
    return False


def user1_dislike_user2(news_id, user1_id, user2_id):
    key = str(news_id) + ':' + str(user1_id) + '_to_' + str(user2_id)
    cache.set(key, 0, settings.NEVER_REDIS_TIMEOUT)


# user1对user2点赞
def user1_like_user2(news_id, user1_id, user2_id):
    key = str(news_id) + ':' + str(user1_id) + '_to_' + str(user2_id)
    cache.set(key, 1, settings.NEVER_REDIS_TIMEOUT)


def user_recommendation():
    pass


