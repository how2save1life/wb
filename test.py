# # # -*- coding:utf-8 -*-
# # import requests
# # from bs4 import BeautifulSoup
# #
# # myHeader = {
# # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
# # 'Cookie': 'SINAGLOBAL=3861082712591.071.1581165858283; ULV=1582006968373:3:3:1:8619389612030.329.1582006968051:1581575304369; UOR=,,login.sina.com.cn; SUHB=0nl-Qv9i4tXYwt; ALF=1613634657; SCF=AmGKs65EdeV1mGJPvtNrSMuLgZEOtfiTbG0PEdiMPSq6N9KYNj9rwBGH-O_hFVlwP0yMMEfEd7qG0-6JXnz70Ko.; SSOLoginState=1582006962; _s_tentry=login.sina.com.cn; Apache=8619389612030.329.1582006968051; SUB=_2A25zSJizDeRhGeNP61oR9SzEwj-IHXVQP417rDV8PUNbmtANLULBkW9NTq2iQl2i0_4Ibxvx6G5b-xLd-A3S_UUT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5HHDDeRwSY2i-3EWu51nD65JpX5KMhUgL.Fo-pehn7SKzR1Ke2dJLoI0eLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hyk1h2EeK5t; WBStorage=42212210b087ca50|undefined',
# #     }
# # resp_user = requests.get('https://weibo.cn/3981470921/info', headers=myHeader)
# # soup_user = BeautifulSoup(resp_user.text, 'lxml')
# # print(resp_user.text)
#
# # -*- coding: utf-8 -*-
# """
# Created on Thu Nov 16 10:08:52 2017
#
# @author: li-pc
# """
#
# import jieba
# from sklearn.feature_extraction.text import  TfidfVectorizer
# from sklearn.cluster import KMeans
#
# def jieba_tokenize(text):
#     return jieba.lcut(text)
#
#
# tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
# '''
# tokenizer: 指定分词函数
# lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
# 所以最好是False
# '''
# print ("ok3")
# text_list = ["今天天气真好啊啊啊啊", "小明上了清华大学", \
# "我今天拿到了Google的Offer", "清华大学在自然语言处理方面真厉害"]
#  #需要进行聚类的文本集
# print ("ok1")
#
# corpus = []
# txt = open("data/cut.txt", "r", encoding='utf-8').read().split("\n")
# for str in txt:
#     corpus.append(str)
#
# tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
#
# num_clusters = 3
# km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=1,
#                     init='k-means++',n_jobs=1)
# print ("ok2")
# '''
# n_clusters: 指定K的值
# max_iter: 对于单次初始值计算的最大迭代次数
# n_init: 重新选择初始值的次数
# init: 制定初始值选择的算法
# n_jobs: 进程个数，为-1的时候是指默认跑满CPU
# 注意，这个对于单个初始值的计算始终只会使用单进程计算，
# 并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40,
# 服务器上面有20个CPU可以开40个进程，最终只会开10个进程
# '''
# #返回各自文本的所被分配到的类索引
# result = km_cluster.fit_predict(tfidf_matrix)
#
# print ("Predicting result: ", result)
# from csvOprate import SaveCSV
#
# result=[0,1]
# s = SaveCSV()
# list = s.readCSV2List("data/wb_data1.csv")  # 读取csv到list
# print(list)
# print(len(list))
# for i in range(len(result)):  # 将分类结果写进list
#     list[i + 1][9] = result[i]
# print(list)
# s.writeList2CSV(list, "data/wb_data1.csv")  # list转回csv
from csvOprate import SaveCSV

s = SaveCSV()
s.read_csv_to_mysql("data/wb_data.csv")  # 写入数据库
