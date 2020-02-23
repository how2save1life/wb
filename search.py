# -*- coding:utf-8 -*-
import codecs
import csv
import os
import sys

import requests
import re
from bs4 import BeautifulSoup
import time

import csvOprate

url_template = 'https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g&page={}'  # 要访问的微博搜索接口URL
myHeader = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
    'Cookie': 'SINAGLOBAL=3861082712591.071.1581165858283; ULV=1582006968373:3:3:1:8619389612030.329.1582006968051:1581575304369; UOR=,,login.sina.com.cn; SUHB=0pHhYiO0YfFYbY; ALF=1613975313; SCF=AmGKs65EdeV1mGJPvtNrSMuLgZEOtfiTbG0PEdiMPSq6AWyoJRE_obCSXgse29igNdqZUlAdtm-lRiSYQi547g0.; SSOLoginState=1582006962; _s_tentry=login.sina.com.cn; Apache=8619389612030.329.1582006968051; SUB=_2A25zVmvDDeRhGeNP61oR9SzEwj-IHXVQItoLrDV8PUNbmtAKLXjTkW9NTq2iQjsI9Y3AovXQbXb3XHbP7K5U8PJd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5HHDDeRwSY2i-3EWu51nD65JpX5KMhUgL.Fo-pehn7SKzR1Ke2dJLoI0eLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hnLxK-L1KeL1hyk1h2EeK5t; WBStorage=42212210b087ca50|undefined; webim_unReadCount=%7B%22time%22%3A1582443147226%2C%22dm_pub_total%22%3A5%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A50%2C%22msgbox%22%3A0%7D',
}


# 将正则表达式获取到的标签文字字符串中的数字提取出来
def re_num(str):
    list = re.compile('\d').findall(str)
    if len(list) == 0:
        return '0'
    else:
        return list[0]


# 爬取一页
def clawonepage(keyword, start_time, end_time, page_id):
    resp = requests.get(
        url_template.format(keyword, start_time, end_time, page_id)
        , headers=myHeader)
    soup = BeautifulSoup(resp.text, 'lxml')
    if soup.find(class_='card-wrap').find(class_='card card-no-result s-pt20b40'):
        print('没找到关键词')
    else:
        all_contents = soup.find_all(attrs={'class': 'card-wrap', 'action-type': 'feed_list_item'})
        # 存下包含微博正文的card-wrap ，排除右侧的广告、热搜
    wblog = []  # 保存一页中的每一个微博

    for content in all_contents:
        wb_username = content.find('p', class_='txt')['nick-name']  # 用户名
        wb_text = content.find('p', class_='txt').text.strip()  # 正文
        wb_time = content.select_one(".txt ~ .from").select_one('a').text.strip()  # 微博发布时间

        #  wb_time = content.find('p', class_='txt').p.next_sibling.find('p', class_='from').find('a').text.strip()
        # 要在<p class=text>的兄弟节点找<p class=from>。否则会爬到转发内容（在子节点里）中的时间

        wb_repost = re_num(content.find('div', class_='card-act').find_all('li')[1].text)  # 转发数
        wb_like = re_num(content.find('div', class_='card-act').find_all('li')[2].text)  # 评论数
        wb_comment = re_num(content.find('div', class_='card-act').find_all('li')[3].text)  # 点赞数
        wb_href = content.find('div', 'avator').find('a')['href']  # 微博id ，包含 '?refer_flag=1001030103_' 这部分
        wb_userid = wb_href.split('?')[0][12:]  # 微博用户ID

        # # 用户个人信息
        # user_info_url = 'https:{}/info'
        # resp_user = requests.get(user_info_url.format(wb_userid), headers=myHeader)
        # soup_user = BeautifulSoup(resp_user.text, 'lxml')
        # print(user_info_url.format(wb_userid))
        # addr = soup_user.find('div', class_='WB_cardwrap S_bg2')  # .find_all('li')[1].find('span',class_='pt_detail').text
        # # sex = soup_user.find('div', class_='WB_cardwrap S_bg2').find_all('li')[2].text
        # # 有个反爬 visitor system加了cookie以后就没了，但是还是爬不到 先算了

        # 单条微博 字典
        blog = {
            'wb_id': wb_href,  # 生成一条微博记录的列表
            'wb_username': wb_username,
            'wb_userid': wb_userid,
            'wb_text': wb_text,
            'wb_time': wb_time,
            'wb_repost': wb_repost,
            'wb_like': wb_like,
            'wb_comment': wb_comment,
            'keyword': keyword
        }
        wblog.append(blog)
        print(blog)
        # 防止封号
        time.sleep(2)

    return wblog


# 爬取多页
def clawpages(keyword, start_time, end_time):
    resp = requests.get(url_template.format(keyword, start_time, end_time, '1')
                        , headers=myHeader)
    soup = BeautifulSoup(resp.text, 'lxml')

    # csv表头
    item_list = ['wb_id',
                 'wb_username',
                 'wb_userid',
                 'wb_text',
                 'wb_time',
                 'wb_repost',
                 'wb_like',
                 'wb_comment',
                 'keyword',
                 'sort'
                 ]
    if soup.find(class_='card-wrap').find(class_='card card-no-result s-pt20b40'):
        print('没找到关键词_')
        return
    else:
        page_num = len(soup.find('div', class_='m-page').find_all('li'))  # 获取此时间单位内的搜索页面的总数量，
        print(page_num, '页')
        page_num = int(page_num)
        print(start_time + ' 到 ' + end_time + " 时间单位内搜索结果页面总数为：%d" % page_num)

    wblogs = []  # 此次时间单位内的搜索全部结果先临时用列表保存，后存入数据库
    for page_ in range(page_num):  #
        page_ = page_ + 1  # 下标从零开始
        print('page_%d downloading--' % page_)
        try:
            wblogs.extend(clawonepage(keyword, start_time, end_time, page_))  # 每页调用函数进行微博信息的抓取
            print('page_%d down' % page_)
        except Exception as e:
            print(e)

    # # 写入数据库
    # mh = mysqlHelper(get_db()[0], get_db()[1], get_db()[2], get_db()[3], get_db()[4], int(get_db()[5]))
    # sql = "insert into wb_data(wb_id,wb_username,wb_userid,wb_text,wb_time,wb_repost,wb_like,wb_comment,keyword) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # mh.open()
    # for i in range(len(wblogs)):
    #     mh.cud(sql, (
    #         wblogs[i]['wb_id'], wblogs[i]['wb_username'], wblogs[i]['wb_userid'], wblogs[i]['wb_text'],
    #         wblogs[i]['wb_time'], wblogs[i]['wb_repost'], wblogs[i]['wb_like'], wblogs[i]['wb_comment']
    #         , keyword))
    # mh.commit_()
    # mh.close()

    # 写入 .csv
    for blog in wblogs:
        s = csvOprate.SaveCSV()
        s.save(item_list, "data/wb_data.csv", blog)
    # read_csv_to_mysql("data/wb_data.csv")


if __name__ == '__main__':
    clawpages('勒索病毒',
              '2019-09-01',
              '2019-12-24')
