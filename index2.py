import os
import re
from shaungxiang import doubleMax

dict1 = {}  # 存储倒排索引，Key和对应的[文档，文档内词频]
dict2 = {}  # 存储总的词频

def prune(txt):
    # 去除标点符号，保留姓名中间的·
    # t=re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])" ,"",txt)
    punctuation = "~!@#$%^&*()_+`{}|\[\]\:\";\='<>?,/"
    t = re.sub('[,+=:：;。，、?!(){}*“”]', '', txt)
    return t

def cutfile(path,resultpath):
    i = 1
    list = os.listdir(path)
    list.sort();
    for dir in list:
        print(str(i))
        child_dir = os.path.join(path, dir)
        new_dir = os.path.join(resultpath,dir)
        with open(child_dir, mode='r', encoding='utf-8') as file:
            data = file.readlines()
            data = [line.strip() for line in data]
        data[0] = prune(data[0])
        data[1] = prune(data[1])
        title = doubleMax(data[0], 'ChineseDic.txt')
        description = doubleMax(data[1], 'ChineseDic.txt')
        f = open(new_dir, mode='a+', encoding='utf-8')
        for words in title or description:
            f.write(str(words)+' ')
        f.close()
        i=i+1


# 构建倒排索引
def invertindex(txtname, txtdata0, txtdata1):
    tmpdict = dict()  # 统计某词在本txt内的词频
    tmpset = set(txtdata0 + txtdata1)  # 统计一个文档内所有单词
    for d in txtdata0:
        if not d.isspace():  # 去掉空格
            if d not in dict1:
                dict1[d] = list()
                dict2[d] = 1  # 统计总的词频
                tmpdict[d] = 1
            else:
                dict2[d] = dict2[d] + 1
                if d not in tmpdict:
                    tmpdict[d] = 1
                else:
                    tmpdict[d] = tmpdict[d] + 1
    for d in txtdata1:
        if not d.isspace():
            if d not in dict1:
                dict1[d] = list()
                dict2[d] = 1  # 统计总的词频
                tmpdict[d] = 1
            else:
                dict2[d] = dict2[d] + 1
                if d not in tmpdict:
                    tmpdict[d] = 1
                else:
                    tmpdict[d] = tmpdict[d] + 1
    # print(tmpset)
    for s in tmpset:
        if not s.isspace():
            dict1[s].append([txtname, tmpdict[s]])
    dict=sorted(dict1.items(),reverse=False)


def display():
    for i in dict1.keys():
        print((i) + ': ' + str(dict2[i]) + '\n' + str(dict1[i]))


def main():
    path = "renamed"
    i = 1
    list = os.listdir(path)
    list.sort();
    for dir in list:
        print(str(i))
        child_dir = os.path.join(path, dir)
        # print(child_dir)
        with open(child_dir, mode='r',encoding='utf-8') as file:
            data = file.readlines()
            data = [line.strip() for line in data]
        # print(data[0])
        # print(data[1])
        # print("去除标点等后：" + prune(data[0]))
        # print("去除标点等后：" + prune(data[1]))
        data[0] = prune(data[0])
        data[1] = prune(data[1])
        # print(doubleMax(data[0], 'ChineseDic.txt'))
        # print(doubleMax(data[1], 'ChineseDic.txt'))
        invertindex(dir, doubleMax(data[0], 'ChineseDic.txt'), doubleMax(data[1], 'ChineseDic.txt'))

        # print('\n')
        # display()

        # print('\n')
        i = i + 1


#main()
#display()
cutfile('renamed','cutresults')