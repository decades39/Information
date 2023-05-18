import os
import re
import math

dict1 = {}
dict2 = {}

isCalculate = 0
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
    # 只计算一遍
    global isCalculate
    if isCalculate == 0:
        # 统计文档词数及总文档数
        for word in dict1.keys():
            # 计算每个文档的总词数
            word_docs = dict1[word]
            for doct in word_docs.keys():
                if doct not in num_doc:
                    num_doc[doct] = int(dict1[word][doct])
                else:
                    num_doc[doct] += int(dict1[word][doct])
        global total_doc
        total_doc = len(num_doc)
        # print("-----文档词数------")
        # print(num_doc)
        # print("-----总文档数-------")
        # print(total_doc)

        isCalculate = 1


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
    # Calculate()
    # 计算所有IDF
    for i in dict1.keys():
        word_docs = dict1[i]
        size = len(word_docs)
        idf[i] = math.log(total_doc / size)
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
    # print(tf_idf)
    for w in dict1.keys():
        for d in dict1[w].keys():
            print("words: " + str(w) + " in  dict: " + str(d) + " = " + str(tf_idf[w][d]))


def TF(ti, dj):
    # 计算单个TF
    if dj not in dict1[ti].keys():
        num_t_in_d = 0
    else:
        num_t_in_d = dict1[ti][dj]
    #num_t_in_d：词ti在文档dj中出现的次数
    # num_doc[dj]:文档dj包含的词数
    tf_t_d = int(num_t_in_d) / int(num_doc[dj])
    # print("TF(" + str(ti) + ", " + str(dj) + ")=num_t_in_d " + str(num_t_in_d) + "/  num_doc[" + str(dj) + "]( " + str(num_doc[dj]) + ")= " + str(tf_t_d))
    return tf_t_d


def IDF(t):
    # 计算单个IDF
    docs = len(dict1[t])
    # docs:包含t的文档数  total_doc:总文档数
    idf_t = math.log(total_doc / docs)
    return idf_t


def TF_IDF(t, d):
    # Calculate()
    tf_idf_td = TF(t, d) * IDF(t)
    print(
        "TF(" + str(t) + ", " + str(d) + ")( " + str(TF(t, d)) + ") * IDF(" + str(t) + ")(" + str(IDF(t)) + ")= " + str(
            tf_idf_td))
    return tf_idf_td


def Score(q, d):
    Calculate()
    result = 0
    for i in q:
        if i in dict1.keys():
            result += TF_IDF(i, d)
    return result


# -----------------------------------------以下为处理Bool类型的函数————————————————————————————————————————————————————————————————


# 用于获取文件名对应的序号
def Getnum(s):
    num_s = s[0:3]
    num = int(num_s)
    return num


# 用于将词汇转化为包含该词汇的文档组成的列表
def dictolist(a):
    list_a = []
    if a in dict1.keys():
        doc_a = dict1[a]
        for key in doc_a.keys():
            list_a.append(key)
    print("------------------list_a--------------------------------")
    print(list_a)
    return list_a


# 注意为在多个与或(MoreAnd/MoreOr)中重用，这里将dictolist的功能剔除，使用时需要自己用dictolist将词语转化为该词所在的文档列表
# 例如： And(dictolist("2020"), dictolist("还有"))
#       Or(dictolist("完成"), dictolist("秀"))
#       Not(dictolist("秀"), dictolist("完成"))
def And(a, b):
    res = []
    size_a = len(a)
    size_b = len(b)
    # print(str(size_a) + " " + str(size_b))
    i = 0
    j = 0
    while i < size_a and j < size_b:
        # print("i: " + str(i) + "  j: " + str(j))
        # print("list_a[" + str(i) + "]= " + str(a[i]) + "; " + " list_b[" + str(j) + "]= " + str(b[j]) + "; ")
        if Getnum(a[i]) == Getnum(b[j]):
            res.append(a[i])
            # print(str(a[i]))
            i += 1
            j += 1
        elif Getnum(a[i]) < Getnum(b[j]):
            i += 1
        else:
            j += 1
    # print(res)
    return (res)


def Or(a, b):
    res = []
    size_a = len(a)
    size_b = len(b)
    # print(str(size_a) + " " + str(size_b))
    i = 0
    j = 0
    while i < size_a and j < size_b:
        # print("i: " + str(i) + "  j: " + str(j))
        # print("list_a[" + str(i) + "]= " + str(a[i]) + "; " + " list_b[" + str(j) + "]= " + str( b[j]) + "; ")
        if Getnum(a[i]) == Getnum(b[j]):
            res.append(a[i])
            # print(str(a[i]))
            i += 1
            j += 1
        elif Getnum(a[i]) < Getnum(b[j]):
            res.append(a[i])
            # print(str(a[i]))
            i += 1
        else:
            res.append(b[j])
            # print(str(b[j]))
            j += 1
    while i < size_a:
        # print("list_a[" + str(i) + "]= " + str(a[i]))
        res.append(a[i])
        # print(str(a[i]))
        i += 1
    while j < size_b:
        # print(" list_b[" + str(j) + "]= " + str(b[j]) + "; ")
        res.append(b[j])
        # print(str(b[j]))
        j += 1
    # print(res)
    return res


def Not(a, b):
    res = []
    size_a = len(a)
    size_b = len(b)
    # print(str(size_a) + " " + str(size_b))
    i = 0
    j = 0
    while i < size_a and j < size_b:
        # print("i: " + str(i) + "  j: " + str(j))
        # print("list_a[" + str(i) + "]= " + str(a[i]) + "; " + " list_b[" + str(j) + "]= " + str(
        #     b[j]) + "; ")
        if Getnum(a[i]) == Getnum(b[j]):
            i += 1
            j += 1
        elif Getnum(a[i]) < Getnum(b[j]):
            res.append(a[i])
            # print(str(a[i]))
            i += 1
        else:
            j += 1
    while i < size_a:
        # print("list_a[" + str(i) + "]= " + str(a[i]))
        res.append(a[i])
        # print(str(a[i]))
        i += 1
    print(res)
    return res


def MoreAnd(words):
    # 将word按照存在的文件数由小到大排列
    doc_seqs = {}
    for word in words:
        if word in dict1.keys():
            temp = dict1[word]
            length = len(temp)
            doc_seqs[word] = length
        else:
            doc_seqs[word] = 0
    print(doc_seqs)
    seq_sort = sorted(doc_seqs.items(), key=lambda x: x[1])
    print("--------------------------排序结果--------------------------------")
    print(seq_sort)
    # 从小到大一一进行And
    num = len(words)
    i = 2
    result = And(dictolist(seq_sort[0][0]), dictolist(seq_sort[1][0]))
    while i < num:
        result = And(result, dictolist(seq_sort[i][0]))
        i += 1
    print("---------------------------------Boolean处理结果-------------------------------")
    print(result)
    return result


def MoreOr(words):
    # 将word按照存在的文件数由大到小排列
    doc_seqs = {}
    for word in words:
        if word in dict1.keys():
            temp = dict1[word]
            length = len(temp)
            doc_seqs[word] = length
        else:
            doc_seqs[word] = 0
    print(doc_seqs)
    seq_sort = sorted(doc_seqs.items(), key=lambda x: x[1], reverse=True)
    print("--------------------------排序结果--------------------------------")
    print(seq_sort)
    # 从大到小一一进行Or
    num = len(words)
    i = 2
    result = Or(dictolist(seq_sort[0][0]), dictolist(seq_sort[1][0]))
    while i < num:
        result = Or(result, dictolist(seq_sort[i][0]))
        i += 1
    print("---------------------------------Boolean处理结果-------------------------------")
    print(result)
    return result

def More(words,operators):
    # opn_and = 0
    # opn_or = 0
    # ope = ""
    # operator = []
    # word_num = []
    # for op in operators:
    #     if op == "and" and ope == "or":
    #         ope = "and"
    #         opn_and += 1
    #         opn_or = 0
    #         if opn_and>1:
    #             operator.append("ormore")
    #             word_num.append(opn_or)
    #         else:
    #             operator.append("or")
    #
    #     elif op == "or":
    #         ope = "or"
    #         opn_or += 1
    #     elif op == "andnot":
    #
    result = dictolist(words[0])
    for i in range(len(operators)):
        if operators[i] == "and":
            result = And(result, dictolist(words[i+1]))
            i += 1
        elif operators[i] == "or":
            result = Or(result, dictolist(words[i+1]))
            i += 1
        elif operators[i] == "andnot":
            result = Not(result, dictolist(words[i + 1]))
            i += 1
    return result





# ---------------------------------------最终处理函数------------------------------------------
def progress(types, wordlist, operatorlist=None):
    if operatorlist is None:
        operatorlist = []
    result = []
    if types == "And":
        docs = And(dictolist(wordlist[0]), dictolist(wordlist[1]))
    elif types == "Or":
        docs = Or(dictolist(wordlist[0]), dictolist(wordlist[1]))
    elif types == "Not":
        docs = Not(dictolist(wordlist[0]), dictolist(wordlist[1]))
    elif types == "MoreAnd":
        docs = MoreAnd(wordlist)
    elif types == "MoreOr":
        docs = MoreOr(wordlist)
    elif types == "Onlyone":
        docs = Or(dictolist(wordlist[0]), [])
    elif types == "More":
        docs = More(wordlist, operatorlist)

    for dicts in docs:
        score = Score(wordlist, dicts)
        result.append((dicts, score))
        print("the score of  words  in doctment " + dicts + " is " + str(score))
        print("-------------------------------------------------------------------------------")
    # print(result)
    result_s = sorted(result, key=lambda x: x[1], reverse=True)
    # print("---------------------------------按评分排序----------------------------------------------")
    # print(result_s)
    return result_s


if __name__ == '__main__':
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    # TF_IDF_all()

    # for w in dict1.keys():
    #     for d in dict1[w].keys():
    #         res = TF_IDF(w, d)
    #         print("words: " + str(w) + " in  dict: " + str(d) + " = " + str(res))

    # And(dictolist("还有"), dictolist("首日"))
    # And(dictolist("2020"), dictolist("还有"))
    # Or(dictolist("完成"), dictolist("秀"))
    # Not(dictolist("秀"), dictolist("完成"))
    # Not(dictolist("前"), dictolist("十"))
    # Not(dictolist("首日"), dictolist("前瞻"))

    # words = ["2020", "的", "运动", "东京"]
    # res = MoreAnd(words)
    # print(dict1)

    # words = ["分组", "揭晓", "球星", "主场", "这里"]
    # docs = MoreOr(words)

    word = ["举办", "竞技体操", "展望", "抽签", "出炉", "你好", "Hello"]
    result = progress("MoreAnd", word)
    print("---------------------------------最终结果----------------------------------------------")
    print(result)

    # words = ["还有", "2020"]
    # # progress()第一个参数为操作类型，包括"Onlyone" “And” “Or” "Not" "MoreAnd" "MoreOr"五种
    # result = progress("And", words)
    # print("---------------------------------最终结果----------------------------------------------")
    # print(result)

    # dictolist("你好")
    # dictolist("还有")
    # words = ["你好"]
    # # progress()第一个参数为操作类型，包括"Onlyone" “And” “Or” "Not" "MoreAnd" "MoreOr"五种
    # result = progress("Onlyone", words)
    # print("---------------------------------最终结果----------------------------------------------")
    # print(result)