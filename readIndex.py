import os
import re
import math

dict1 = {}
dict2 = {}

total_doc = 0  # 文件总数
num_doc = {}  # 文档内总词数
tf = {}
idf = {}
tf_idf = {}


def readIndex(filepath):
    index = open(filepath, mode='r', encoding='utf-8')
    line = index.readline().strip()
    linenum = 1
    while line:
        print(linenum)
        temp = re.split(' ---->|:', line)
        size = len(temp)
        # dict1[temp[0]] = list()
        dict1[temp[0]] = {}
        dict2[temp[0]] = temp[1]
        for i in range(size):
            if i > 1 & i % 2 == 0:
                txt = temp[i]
                num = temp[i + 1]
                # print(' ',txt, ' ', num)
                # dict1[temp[0]].append([txt, num])
                dict1[temp[0]][txt] = num
        line = index.readline().strip()
        linenum += 1


def Calculate():
    # 统计文档词数及总文档数
    for word in dict1.keys():
        # 计算每个文档的总词数
        word_docs = dict1[word]
        # print(word_docs)
        for doc in word_docs.keys():
            # print(doc)
            if doc not in num_doc:
                # print(dict1[word][doc])
                num_doc[doc] = int(dict1[word][doc])
            else:
                num_doc[doc] += int(dict1[word][doc])
    global total_doc
    total_doc = len(num_doc)
    print("-----文档词数------")
    print(num_doc)
    print("-----总文档数-------")
    print(total_doc)


def TF_all():
    Calculate()
    # 计算所有的TF
    for words in dict1.keys():
        for docs in num_doc.keys():
            if docs not in dict1[words]:
                num = 0
            else:
                num = dict1[words][docs]
            tf_w_d = int(num) / int(num_doc[docs])
            # if tf_w_d != 0:
            # print("Words: " + words + " Docs:" + docs)
            # print("num= " + str(num) + " total= " + str(num_doc[docs]) +" tf= "+str(tf_w_d))
            if words not in tf:
                tf[words] = {}
            tf[words][docs] = tf_w_d
    print("-----TF------")
    print(tf)


def IDF_all():
    #Calculate()
    # 计算所有IDF
    for i in dict1.keys():
        word_docs = dict1[i]
        size = len(word_docs)
        idf[i] = math.log( total_doc / size)
    print("-----IDF------")
    print(idf)


def TF_IDF_all():
    TF_all()
    IDF_all()
    # 计算所有TF_IDF
    for words in dict1.keys():
        for docs in num_doc.keys():
            result = tf[words][docs] * idf[words]
            if words not in tf_idf:
                tf_idf[words] = {}
            tf_idf[words][docs] = result
    print("-----TF_IDF------")
    print(tf_idf)


def TF(ti, dj):
    Calculate()
    num_t_in_d = dict1[ti][dj]
    tf_t_d = int(num_t_in_d) / int(num_doc[dj])
    return tf_t_d


def IDF(t):
    docs = len(dict1[t])
    idf_t = math.log(total_doc / docs)
    return idf_t


def TF_IDF(t, d):
    tf_idf_td = TF(t, d) * IDF(t)
    return tf_idf_td


def Score(q, d):
    result = 0
    for i in q:
        result += TF_IDF(i, d)
    return result


if __name__ == '__main__':
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    # print(dict1)
    # for i in dict1.keys():
    #     print((i) + ': ' + str(dict2[i]) + '\n' + str(dict1[i]))
    TF_IDF_all()
