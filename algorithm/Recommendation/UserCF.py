# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 12:07
# @Author  : 陈强
# @FileName: UserCF.py
# @Software: PyCharm



from datetime import datetime
from datetime import timedelta
from math import sqrt
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsRecommendation.settings")
django.setup()
from user.models import user_tag_score, user_similarity, user_behavior

"""基于用户的协同过滤算法，根据用户兴趣矩阵计算相似用户，用户量过大时计算量过大，不利于在线计算，用于离线计算相似用户"""


class CalculateSimilarityUser(object):
    def __init__(self):
        pass

    def get_data(self):
        # 取出所有的用户兴趣数据
        datas = user_tag_score.objects.all().values_list()

        # [[用户id,(兴趣分数tuple)],...]
        data_list = []
        for data in datas:
            user_list = []
            user_list.append(data[0])
            user_list.append(data[1:])
            data_list.append(user_list)
        return data_list

    def update_data(self, similarity_user_dict):
        user = user_similarity.objects.filter(user_id=similarity_user_dict['user_id'])
        if user.exists():
            user.update(similary_user=similarity_user_dict['similary_user'])
        else:
            user_similarity.objects.create(**similarity_user_dict)

    def cal_pearson(self, x, y):

        def multiply(a, b):
            # a,b两个列表的数据一一对应相乘之后求和
            sum_ab = 0.0
            for i in range(len(a)):
                temp = a[i] * b[i]
                sum_ab += temp
            return sum_ab

        n = len(x)
        # 求x_list、y_list元素之和
        sum_x = sum(x)
        sum_y = sum(y)
        # 求x_list、y_list元素乘积之和
        sum_xy = multiply(x, y)
        # 求x_list、y_list的平方和
        sum_x2 = sum([pow(i, 2) for i in x])
        sum_y2 = sum([pow(j, 2) for j in y])
        molecular = sum_xy - (float(sum_x) * float(sum_y) / n)
        # 计算Pearson相关系数，molecular为分子，denominator为分母
        denominator = sqrt((sum_x2 - float(sum_x ** 2) / n) * (sum_y2 - float(sum_y ** 2) / n))
        if denominator == 0:
            return 0
        return molecular / denominator

    """计算相似的用户，并更新到数据库中，k为最相似的k个用户"""

    def similarity_user(self, k=10):
        data_list = self.get_data()
        # 相似用户矩阵:[[user_id,(user_id,score).....]...]
        similarity_user_matrix = [[i[0]] for i in data_list]

        for i in range(len(data_list)):
            user_id_i = data_list[i][0]
            score_tuple_i = data_list[i][1]

            for j in range(i + 1, len(data_list), 1):
                user_id_j = data_list[j][0]
                score_tuple_j = data_list[j][1]

                pearson = self.cal_pearson(score_tuple_i, score_tuple_j)

                similarity_user_matrix[i].append((user_id_j, pearson))
                # 直接添加到后面的相似用户中，避免重复计算
                similarity_user_matrix[j].append((user_id_i, pearson))

        for i in similarity_user_matrix:
            user_id = i[0]
            user_tuple = i[1:]
            sorted_list = sorted(user_tuple, key=lambda user: user[1], reverse=True)

            # 相似用户，保存为字符串，用，隔开，存入数据库中
            similary_user = ''
            for j in sorted_list[:k]:
                similary_user += str(j[0]) + ','
            similarity_user_dict = {'user_id': user_id, 'similary_user': similary_user[:-1]}
            print(similarity_user_dict)
            self.update_data(similarity_user_dict)


"""根据数据库中的相似用户表进行推荐"""


class UserCFRecommendation(object):
    def __init__(self):
        pass

    def get_days_before_today(self, days=2):
        return datetime.now() - timedelta(days=days)

    def get_data(self, user_id):
        user = user_similarity.objects.filter(user_id=user_id)
        if user.exists():
            before_today = self.get_days_before_today()
            news_list = user_behavior.objects.filter(user_id=user_id, behavior_type__in=[1, 2],
                                                     behavior_time__range=[before_today, datetime.now()]).values_list(
                'news_id', flat=True)
            # 当前用户浏览资讯集合
            user_set = set(news_list)
            # 相似用户浏览资讯集合
            similary_user_set = set()
            # 取出和该用户相似的用户id
            similary_user_list = user[0].similary_user.split(',')

            for similary_user in similary_user_list:
                # 取出相似用户浏览过的资讯
                news_list = user_behavior.objects.filter(user_id=int(similary_user), behavior_type__in=[1, 2],
                                                         behavior_time__range=[before_today,
                                                                               datetime.now()]).values_list('news_id',
                                                                                                            flat=True)
                similary_user_set.update(news_list)

            # 取差集，即推荐的资讯id集合
            difference_set = similary_user_set.difference(user_set)
            # print(difference_set)
            return difference_set
        else:
            return None


if __name__ == '__main__':
    CalculateSimilarityUser().similarity_user()
    # UserCF_Recommendation().get_data(2)
    # print(3.32780127197021e-59**2)
