# -*- coding:utf-8 -*-
# 写入.csv文件
import codecs
import csv
import os

from Mysql import mysqlHelper, get_db


class SaveCSV(object):

    def save(self, keyword_list, path, item):
        """
        保存csv方法
        :param keyword_list: 保存文件的字段或者说是表头
        :param path: 保存文件路径和名字
        :param item: 要保存的字典对象
        :return:
        """
        try:
            # 第一次打开文件时，第一行写入表头
            if not os.path.exists(path):
                with open(path, "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
                    writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                    writer.writeheader()  # 写表头的方法

            # 接下来追加写入内容
            with open(path, "a", newline='', encoding='utf-8') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
                writer.writerow(item)  # 按行写入数据
                print("写入成功")

        except Exception as e:
            print("write error==>", e)
            # 记录错误数据
            # with open("error.txt", "w") as f:
            #     f.write(json.dumps(item) + ",\n")
            pass

    def readCSV2List(self, Path):
        try:
            file = open(Path, 'r', encoding="utf-8")  # 读取以utf-8
            context = file.read()  # 读取成str
            list_result = context.split("\n")  # 以回车符\n分割成单独的行
            # 每一行的各个元素是以【,】分割的，因此可以
            length = len(list_result)
            for i in range(length):
                list_result[i] = list_result[i].split(",")
            return list_result
        except Exception:
            print("文件读取转换失败，请检查文件路径及文件编码是否正确")
        finally:
            file.close();  # 操作完成一定要关闭

    def writeList2CSV(self, myList, filePath):
        try:
            with open(filePath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(myList)
                print("list->csv成功")
        except Exception as e:
            print(e, "数据写入失败，请检查文件路径及文件编码是否正确")
        # finally:
        #     file.close();  # 操作完成一定要关闭

    def read_csv_to_mysql(self, filename):
        with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            head = next(reader)
            print(head)
            mh = mysqlHelper(get_db()[0], get_db()[1], get_db()[2], get_db()[3], get_db()[4], int(get_db()[5]))
            sql = 'insert into wb_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mh.open()
            for item in reader:
                # if item[1] is None or item[1] == '':  # item[1]作为唯一键，不能为null
                #     continue
                args = tuple(item)
                print(args)
                mh.cud(sql, args)
            mh.commit_()
            mh.close()
