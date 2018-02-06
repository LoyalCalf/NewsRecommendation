# # -*- coding: utf-8 -*-
# # @Time    : 2018/2/5 16:25
# # @Author  : 陈强
# # @FileName: NaiveBayes.py
# # @Software: PyCharm
# import os
#
# class NaiveBayes(object):
#     def __init__(self,train_folder_path,model_file_path):
#         # self.train_data_file = open(train_data_file,"r")
#         # self.model_file = open(model_file,'w')
#         self.train_folder_path = train_folder_path
#         self.model_file_path = model_file_path
#         #存储每一种类型出现的次数
#         self.class_count = {}
#         #存储每一种类型下各个单词出现的次数
#         self.class_word_count = {}
#         #唯一单词总数
#         self.unique_words = {}
#
#         #===========贝叶斯参数============#
#         #每个类别的先验概率
#         self.class_probabilities = {}
#         #拉普拉斯平滑，防止概率为0的情况出现
#         self.laplace_smooth = 0.1
#         #模型训练结果集
#         self.class_word_prob_matrix = {}
#         #当某个单词在某类别下不存在时，默认的概率（拉普拉斯平滑后）
#         self.class_default_prob = {}
#
#     # def __del__(self):
#     #     self.train_data_file.close()
#     #     self.model_file.close()
#
#     def loadData(self):
#         file_list = os.listdir(self.train_folder_path)
#         for file in file_list:
#             with open('./afterCutWords/'+file,'r',encoding='utf8') as f:
#                 words = f.read().split()
#             category = file[:-4]
#             if category not in self.class_count:
#                 self.class_count[category] = 0
#                 self.class_word_count[category] = {}
#                 self.class_word_prob_matrix[category] = {}
#
#             self.class_count[category] += 1
#
#             for word in words:
#                 if word not in self.unique_words:
#                     self.unique_words[word] = 1
#                 if word not in self.class_word_count[category]:
#                     self.class_word_count[category][word] = 1
#                 else:
#                     self.class_word_count[category][word] += 1
#
#         # while len(line)>0:
#         #     words = line.split('#')[0].split()
#         #     category = words[0]
#         #     if category not in self.class_count:
#         #         self.class_count[category] = 0
#         #         self.class_word_count[category] = {}
#         #         self.class_word_prob_matrix[category] = {}
#         #
#         #     self.class_count[category] += 1
#         #
#         #     for word in words[1:]:
#         #         word_id = int(word)     #取得唯一id描述
#         #         if word_id not in self.unique_words:
#         #             self.unique_words[word_id] = 1
#         #         if word_id not in self.class_word_count[category]:
#         #             self.class_word_count[category][word_id] = 1
#         #         else:
#         #             self.class_word_count[category][word_id] += 1
#         #
#         #     line = self.train_data_file.readline().strip()
#         #     line_num += 1
#             # print (line_num,'training instances loaded')
#         print(len(self.class_count),"categories!",len(self.unique_words),"words!")
#
#     def computeModel(self):
#         #计算P(Yi)
#         news_count = 0
#         for count in self.class_count.values():
#             news_count += count
#         for class_id in self.class_count.keys():
#             self.class_probabilities[class_id] = float(self.class_count[class_id])/news_count
#
#         #计算P(X|Yi)<=====>计算所有P(Xi|Yi)的积<=====>计算所有Log(P(Xi|Yi))的和
#         for class_id in self.class_word_count.keys():
#             #当前类别下所有单词的总数
#             sum = 0.0
#             for word_id in self.class_word_count[class_id].keys():
#                 sum += self.class_word_count[class_id][word_id]
#
#             count_Yi = (float)(sum + len(self.unique_words)*self.laplace_smooth)
#             #计算单个单词在某类别下的概率，存储在结果矩阵中，
#             # 所有当前类别没有的单词赋以默认概率（即使用拉普拉斯平滑）
#             for word_id in self.class_word_count[class_id].keys():
#                 self.class_word_prob_matrix[class_id][word_id] = (float)(self.class_word_count[class_id][word_id] + self.laplace_smooth)/count_Yi
#             self.class_default_prob[class_id] = (float)(self.laplace_smooth)/count_Yi
#             print(class_id,'matrix finished,length=',len(self.class_word_prob_matrix[class_id]))
#
#
#     def saveModel(self):
#         #把每个分类的先验概率写入文件
#         with open(self.model_file_path,'w',encoding='utf8') as model_file:
#
#             for class_id in self.class_probabilities.keys():
#                 model_file.write(class_id)
#                 model_file.write(' ')
#                 model_file.write(str(self.class_probabilities[class_id]))
#                 model_file.write(' ')
#                 model_file.write(str(self.class_default_prob[class_id]))
#                 model_file.write('#')
#
#             model_file.write('\n')
#             #把每个单词在当前类别的概率写入文件
#             for class_id in self.class_word_prob_matrix.keys():
#                 model_file.write(class_id+' ')
#                 for word_id in self.class_word_prob_matrix[class_id].keys():
#                     model_file.write(str(word_id)+' '\
#                             + str(self.class_word_prob_matrix[class_id][word_id]))
#                     model_file.write(' ')
#                 model_file.write('\n')
#
#
#     def train(self):
#         self.loadData()
#         self.computeModel()
#         self.saveModel()
#
# if __name__ == '__main__':
#     nb = NaiveBayes('./afterCutWords','./trainModel/trainModel.txt')
#     nb.train()