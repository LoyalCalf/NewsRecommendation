# import os
# import re
# import jieba
# import jieba.analyse
# import random
#
# class DataPerpare(object):
#     def __init__(self):
#         #存放训练数据的文件夹，训练数据统一为txt文件
#         # self.dataDir = dataDir
#         jieba.analyse.set_stop_words('stop_words.txt')
#
#         # 一个包含所有不重复单词的集合====unique_words
#         self.unique_words = set()
#
#
#     def TextProcessing(self,folder_path):
#         folder_list = os.listdir(folder_path)  # 查看folder_path下的文件
#         data_list = []  # 数据集数据
#         class_list = []  # 数据集类别
#
#         # 遍历每个子文件夹
#         for folder in folder_list:
#             new_folder_path = os.path.join(folder_path, folder)  # 根据子文件夹，生成新的路径
#             files = os.listdir(new_folder_path)  # 存放子文件夹下的txt文件的列表
#             word_list = []
#             # 遍历每个txt文件
#             for file in files:
#                 with open(os.path.join(new_folder_path, file), 'r', encoding='utf-8') as f:  # 打开txt文件
#                     raw = f.read()
#
#                 #提取每篇新闻的20个关键字作为新闻特征字
#                 feature = jieba.analyse.extract_tags(raw, 20)
#                 for tag in feature:
#                     word_list.append(tag)
#             with open(r'./afterCutWords/'+folder+'.txt','w',encoding='utf8') as f:
#                 for i in word_list:
#                     f.write(i+' ')
#         #         data_list.append(feature)
#         #         word_cut = jieba.cut(raw, cut_all=False)  # 精简模式，返回一个可迭代的generator
#         #         word_list = list(word_cut)  # generator转换为list
#         #
#         #         data_list.append(word_list)  # 添加数据集数据
#         #         class_list.append(folder)  # 添加数据集类别
#         #         j += 1
#         #
#         # data_class_list = list(zip(data_list, class_list))  # zip压缩合并，将数据与标签对应压缩
#         # random.shuffle(data_class_list)  # 将data_class_list乱序
#         # index = int(len(data_class_list) * test_size) + 1  # 训练集和测试集切分的索引值
#         # train_list = data_class_list[index:]  # 训练集
#         # test_list = data_class_list[:index]  # 测试集
#         # train_data_list, train_class_list = zip(*train_list)  # 训练集解压缩
#         # test_data_list, test_class_list = zip(*test_list)  # 测试集解压缩
#         #
#         # all_words_dict = {}  # 统计训练集词频
#         # for word_list in train_data_list:
#         #     for word in word_list:
#         #         if word in all_words_dict.keys():
#         #             all_words_dict[word] += 1
#         #         else:
#         #             all_words_dict[word] = 1
#         #
#         # # 根据键的值倒序排序
#         # all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f: f[1], reverse=True)
#         # all_words_list, all_words_nums = zip(*all_words_tuple_list)  # 解压缩
#         # all_words_list = list(all_words_list)  # 转换成列表
#         # return all_words_list, train_data_list, test_data_list, train_class_list, test_class_list
#
#
#
#     # cate为feature特征词集合所属的类别
#     # def writeFeature(self, cate, feature):
#     #     self.fn.write(cate + ' ')
#     #     for word in feature:
#     #         if word not in self.word_ids:
#     #             self.unique_words.append(word)
#     #             # 使用unique_words当前数组长度作为单词的唯一id
#     #             self.word_ids[word] = len(self.unique_words)
#     #
#     #             #将单词与对应id写入单词：id字典文件
#     #             self.fd.write(word + ' ' + str(self.word_ids[word]) + ' ')
#     #         self.fn.write(str(self.word_ids[word]) + ' ')
#     #     self.fn.write('#' + cate + '\n')
#     #
#     # def getDataFilenames(self,dir):
#     #     fileList = []
#     #     for dirpath, dirnames, filenames in os.walk(self.dataDir):
#     #         break
#     #
#     #     for filename in filenames:
#     #         # 过滤非excel文件
#     #         m = re.search(r"xlsx", filename)
#     #         if not m:
#     #             continue
#     #         fileList.append(filename)
#     #     return fileList
#     #
#     # def loadWord_id_dict(self):
#     #     fd = open(dirPath + "/system/classPredict/NavieBayesInfo/word_id_dict.txt", 'r',encoding='utf8')
#     #     allInfo = fd.read()
#     #     arr = allInfo.strip().split()
#     #     for i in range(0, len(arr)):
#     #         if i % 2 == 0:
#     #             self.word_ids[arr[i]] = arr[i + 1]
#     #             if arr[i] not in self.unique_words:
#     #                 self.unique_words.append(arr[i])
#
# # dp = DataPerpare(dirPath + "/system/classPredict/trainData")
# # dp.loadWord_id_dict()
# # dp.getNewContentAndAnalyse()
# if __name__=='__main__':
#     DataPerpare().TextProcessing('./trainData')
