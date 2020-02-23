# coding:utf-8


import jieba
import pandas
import codecs
import re

# 处理emoji
def filter_emoji(desstr, restr=''):
    try:
        str = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        str = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return str.sub(restr, desstr)

# 清洗文本
def clearTxt(line:str):
    if(line != ''):
        line = line.strip()
        # 去除文本中的英文和数字
        line = re.sub("[a-zA-Z0-9]", "", line)
        # 去除文本中的中文符号和英文符号
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．|]+|[+——！，。？?、~@#￥%……&*<>《》（）【】{}[\]]+", "", line)
        # 去除emoji
        line = filter_emoji(line, restr='')
        return line
    return None

#文本切割 分词
def sent2word(line):
    segList = jieba.cut(line,cut_all=False)
    segSentence = ''
    for word in segList:
        if word != '\t':
            segSentence += word + " "
    return segSentence.strip()



if __name__ == '__main__':
    df = pandas.read_csv('data/wb_data.csv')
    target = codecs.open('data/cut.txt', 'w', encoding='utf-8')
    for i in df['wb_text']:
        line = clearTxt(i)
        seg_line = sent2word(line)
        target.writelines(seg_line + '\n')

