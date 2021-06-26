# -*- coding: utf-8 -*-
# @Author  : Felix
# @Function: 数据展示（词云，曲线图）

import jieba
import wordcloud
from matplotlib.image import imread
import matplotlib.pyplot as plt

#分词，词云用
def charater_split(text):
    ls = jieba.lcut(text)
    ls = [word for word in ls if len(word.strip())>1] #清洗一个字的词
    txt = " ".join(ls)
    return txt

#读取csv
fo = open("resource/result.csv","r",encoding="UTF-8")
ls = []
for line in fo:
    line = line.replace("\n","")
    line = line.replace("\"","")
    ls.append(line.split(","))
fo.close()
ls.pop(0) #去掉标题


counts_date,counts_pubperson = {},{}
text = ''

for line in ls:
    text += line[3]
    counts_date[line[1]] = counts_date.get(line[1], 0) + 1
    counts_pubperson[line[2]] = counts_pubperson.get(line[2], 0) + 1

#词云
txt = charater_split(text)
mask = imread("resource/1.jpg") #NJIT校徽
w = wordcloud.WordCloud(background_color ="white",font_path="resource/msyh.ttf",mask=mask,max_words=250) #字体：微软雅黑
w.generate(txt)
w.to_file("resource/wordcloud.png")



items1 = list(counts_date.items())
items2 = list(counts_pubperson.items())

#逆序
#items1.sort(key=lambda x:x[1],reverse = True)
items2.sort(key=lambda x:x[1],reverse = True)

date_1, value_1 = [],[]
pub_2, value_2 = [],[]

for k, v in items1:
    date_1.append(k)
    value_1.append(v)
    print("{}:{}".format(k,v))
for k, v in items2:
    pub_2.append(k)
    value_2.append(v)
    print("{}:{}".format(k,v))

#plt绘图
plt.rcParams['font.family']='Fangsong' #中文绘图

#如需切换Part，请注释掉相反Part
#Part1:按照date绘图
'''
plt.plot(date_1,value_1)
date_1 = [date_1[x] for x in range(len(date_1)) if x%16 == 0] #抽取日期，否则x轴坐标无法显示
plt.xticks(date_1,rotation=45)
'''

#Part2:按照pubperson绘图
pub_2 = pub_2[0:25]
value_2 = value_2[0:25]

plt.plot(pub_2,value_2)
plt.xticks(pub_2,rotation=45)

plt.show()

