import os
import re
import math
from shaungxiang import doubleMax
from readIndex import TF_IDF, init_idf

dict1 = {}  # 每个词出现的文档
dict_mc = {}  # Mc 每个词出现的总次数
total_term = 0  # 总词数
dict_md = {}  # Md 文档内的单词
num_doc = {}  # 文档内总词数
total_doc = 0  # 文档总数

pmd = {}
pmc = {}

p = {}
r = {}
n = {}
c = {}

pv = {}
rv = {}
cv = {}
Vi = {}

pv1 = {}
rv1 = {}
cv1 = {}

tf_idf_c = {}

bi_dict_mc = {}  # bi-gram Mc
bi_total_mc = 0  # 总的二元词数
bi_dict_md = {}  # bi-gram Md
bi_num_doc = {}  # Md内bi-gram词数

p1 = {}  # 二元计算时的p1
bi_p2 = {}  # 二元计算时的p2


def readIndex(filepath):
    index = open(filepath, mode='r', encoding='utf-8')
    line = index.readline().strip()
    linenum = 1
    while line:
        # print(linenum)
        temp = re.split(' ---->|:', line)
        size = len(temp)
        # dict1[temp[0]] = list()
        dict1[temp[0]] = {}
        dict_mc[temp[0]] = temp[1]
        global total_term
        total_term += int(temp[1])
        for i in range(size):
            if i > 1 & i % 2 == 0:
                txt = temp[i]
                num = temp[i + 1]
                # print(' ',txt, ' ', num)
                dict1[temp[0]][txt] = num
                if txt not in dict_md:
                    dict_md[txt] = {}
                dict_md[txt][temp[0]] = num
                if txt not in num_doc:
                    num_doc[txt] = 0
                num_doc[txt] += int(num)
        line = index.readline().strip()
        linenum += 1
    global total_doc
    total_doc = len(num_doc)


def write_dict(store_name, dict_temp, dict_count):
    pwd0 = os.getcwd()
    rname = pwd0 + '\\' + store_name + '.txt'
    f = open(rname, mode='a+', encoding='utf-8')
    for i in dict_temp.keys():
        print(i + ': ' + str(dict_count[i]) + '\n' + str(dict_temp[i]))
        f.write(i + ':' + str(dict_count[i]))
        for j in dict_temp[i].keys():
            print(j, ':', str(dict_temp[i][j]))
            f.write(' ---->' + str(j) + ':' + str(dict_temp[i][j]))
        f.write('\n')
    f.close()


def write_mc():
    pwd0 = os.getcwd()
    rname = pwd0 + '\\Mc' + '.txt'
    f = open(rname, mode='a+', encoding='utf-8')
    f.write('Total_Term_Num' + ':' + str(total_term))
    f.write('\n')
    for i in dict_mc.keys():
        f.write(i + ':' + str(dict_mc[i]))
        f.write('\n')
    f.close()


def cal_p_r_c():
    for i in dict_mc.keys():
        p[i] = 0.5
    for j in dict1.keys():
        dic_t = dict1[j]
        n[j] = len(dic_t)
        r[j] = n[j] / total_doc
    for k in dict_mc.keys():
        c[k] = math.log2((p[k] * (1 - r[k])) / (r[k] * (1 - p[k])))
    # print("p:", p)
    # print("r:", r)
    # print("c:", c)


def cal_pmc():
    for i in dict_mc.keys():
        pmc[i] = int(dict_mc[i]) / total_term
    # print("\npmc", pmc)


def cal_pmd():
    for d in dict_md.keys():
        if d not in pmd.keys():
            pmd[d] = {}
        for t in dict_md[d]:
            pmd[d][t] = int(dict_md[d][t]) / int(num_doc[d])


def cal_tf_idf_prc():
    for t in dict_mc.keys():
        if t not in tf_idf_c:
            tf_idf_c[t] = {}
        for d in dict_md.keys():
            if d in dict1[t]:
                tmpp = TF_IDF(t, d)
                tf_idf_c[t][d] = math.log2((tmpp * (1 - r[t])) / (r[t] * (1 - tmpp)))
            else:
                tf_idf_c[t][d] = 0


# 计算初始的式子
def score_init_md_mc(query, lamada):
    dict_score_rmc = {}
    for d in dict_md.keys():
        d_score = 1
        for t in query:
            if t in dict_md[d]:
                t_score = lamada * pmd[d][t] + (1 - lamada) * pmc[t]
            elif t in pmc.keys():
                t_score = (1 - lamada) * pmc[t]
            else:
                t_score = 1
            d_score *= t_score
        dict_score_rmc[d] = d_score
    # 按照评分排序
    result = sorted(dict_score_rmc.items(), key=lambda x: x[1], reverse=True)
    return result


# 计算第一个算式
def score_md_mc(query, lamada, inc):
    dict_score_rmc = {}
    for d in dict_md.keys():
        d_score = 1
        for t in query:
            if t in dict_md[d]:
                # print("t:", t, "d ", d, " c:", inc[t], " lamada:", lamada, " pmc:", pmc[t])
                t_score = lamada * inc[t] + (1 - lamada) * pmc[t]
            elif t in pmc.keys():
                # print(" t:", t, "d ", d, " lamada:", lamada, " pmc:", pmc[t])
                t_score = (1 - lamada) * pmc[t]
            else:
                # print(" t:", t, "d ", d, " lamada:", lamada)
                t_score = 1

            d_score *= t_score
        dict_score_rmc[d] = d_score
    # 按照评分排序
    result = sorted(dict_score_rmc.items(), key=lambda x: x[1], reverse=True)
    return result


# 计算第二个算式
def cal_vi(t, result):
    num = 0
    if t in dict1.keys():
        txts = dict1[t]
        for d in result.keys():
            if d in txts.keys():
                num += 1
    return num


def cal_pv_rv_cv(query, result):
    v = len(result)
    for t in query:
        tmp_vi = cal_vi(t, result)
        Vi[t] = tmp_vi
        if tmp_vi != v:
            pv[t] = tmp_vi / v
        else:
            pv[t] = (tmp_vi * 100) / (v * 100 + 1)
        if t in dict_mc.keys():
            # print("n[t]", n[t], "Vi[t]", Vi[t])
            if n[t] != Vi[t]:
                rv[t] = (n[t] - Vi[t]) / (total_doc - v)
            else:
                rv[t] = (n[t] - Vi[t] + 0.5) / (total_doc - v + 1)
            # print("t", t, "pv", pv[t], "rv", rv[t])
        if pv[t] == 0:
            cv[t] = -10000
        else:
            cv[t] = math.log2((pv[t] * (1 - rv[t])) / (rv[t] * (1 - pv[t])))


# 计算第三个式子

def cal_pv1_rv1_cv1(query, result):
    v = len(result)
    for t in query:
        if t in dict_mc.keys():
            pv1[t] = (Vi[t] + 0.5) / (v + 1)
            rv1[t] = (n[t] - Vi[t] + 0.5) / (total_doc - v + 1)
            cv1[t] = math.log2((pv1[t] * (1 - rv1[t])) / (rv1[t] * (1 - pv1[t])))


# 计算对应tf-idf的式子
def score_tf_idf_md_mc(query, lamada):
    dict_score_rmc = {}
    for d in dict_md.keys():
        d_score = 1
        for t in query:
            if t in dict_md[d]:
                t_score = lamada * tf_idf_c[t][d] + (1 - lamada) * pmc[t]
            elif t in pmc.keys():
                t_score = (1 - lamada) * pmc[t]
            else:
                t_score = 1
            d_score *= t_score
        dict_score_rmc[d] = d_score
    # 按照评分排序
    result = sorted(dict_score_rmc.items(), key=lambda x: x[1], reverse=True)
    return result


# 二元
def bi_gram():
    filepath = os.getcwd() + "\\CutResult1.0.txt"
    bi_f = open(filepath, mode='r', encoding='utf-8')
    line = bi_f.readline().strip()
    while line:
        # 第一行  1 : 24
        temp = re.split(', |:', line)
        file_txt = str(temp[0]).zfill(3) + '.txt'
        # print(file_txt)
        if file_txt not in bi_dict_md:
            bi_dict_md[file_txt] = {}
        if file_txt not in bi_num_doc:
            bi_num_doc[file_txt] = 0
        # 第二行  2020,  年,  东京,  奥运会,  七人制,  橄榄球,  分组,  揭晓,
        line = bi_f.readline().strip()
        temp1 = re.split(', |  |:', line)
        # print("\n", temp1)
        length = len(temp1)
        # print(length)
        i = 0
        while i < length - 1:
            str1 = temp1[i].replace(" ", "")
            str2 = temp1[i + 1].replace(" ", "")
            if tuple[str1, str2] not in bi_dict_md[file_txt]:
                bi_dict_md[file_txt][tuple[str1, str2]] = 1
            else:
                bi_dict_md[file_txt][tuple[str1, str2]] += 1
            if tuple[str1, str2] not in bi_dict_mc:
                bi_dict_mc[tuple[str1, str2]] = 1
            else:
                bi_dict_mc[tuple[str1, str2]] += 1
            bi_num_doc[file_txt] += 1
            global bi_total_mc
            bi_total_mc += 1
            i += 1
        # 第三行 距离,  奥运会,  开幕,  还有,  25,  天,  2020,  年,  东京,  奥运会,  七人制,  橄榄球,  比赛,  分组,  今天,  揭晓,
        line = bi_f.readline().strip()
        temp2 = re.split(',|  |:', line)
        # print("\n", temp2)
        length1 = len(temp2)
        # print(length1)
        j = 0
        while j < length1 - 1:
            str1 = temp2[j].replace(" ", "")
            str2 = temp2[j + 1].replace(" ", "")
            if tuple[str1, str2] not in bi_dict_md[file_txt]:
                bi_dict_md[file_txt][tuple[str1, str2]] = 1
            else:
                bi_dict_md[file_txt][tuple[str1, str2]] += 1
            if tuple[str1, str2] not in bi_dict_mc:
                bi_dict_mc[tuple[str1, str2]] = 1
            else:
                bi_dict_mc[tuple[str1, str2]] += 1
            bi_num_doc[file_txt] += 1
            bi_total_mc += 1
            j += 1
        line = bi_f.readline().strip()
        line = bi_f.readline().strip()
    # print("\nbi_dict_md", bi_dict_md)
    # print("\nbi_num_doc", bi_num_doc)
    # print("\nbi_dict_mc", bi_dict_mc)
    # print("\nbi_total_mc", bi_total_mc)


def cal_p1_p2(lamada):
    for i in dict_mc.keys():
        if i not in p1.keys():
            p1[i] = {}
        for d in dict_md.keys():
            # print("\nd:", d)
            if i in dict_md[d]:
                temp_d = int(dict_md[d][i]) / int(num_doc[d])
            else:
                temp_d = 0
            temp_c = pmc[i]
            p1[i][d] = lamada * temp_d + (1 - lamada) * temp_c
            # print('p1[', i, '][', d, ']  = ', p1[i][d])
    for t2 in bi_dict_mc.keys():
        if t2 not in bi_p2.keys():
            bi_p2[t2] = {}
        for d in dict_md.keys():
            if t2 in bi_dict_md[d]:
                temp_d = int(bi_dict_md[d][t2]) / int(bi_num_doc[d])
            else:
                temp_d = 0
            temp_c = int(bi_dict_mc[t2]) / int(bi_total_mc)
            bi_p2[t2][d] = lamada * temp_d + (1 - lamada) * temp_c

    # print('\n\n\np1:', p1)
    # print('\n\n\nbi_p2:', bi_p2)


def score_bi_gram(query):
    dict_score_bi_gram = {}
    length = len(query)
    for d in dict_md.keys():
        d_score = 1
        for i in range(length):
            if i == 0:
                if query[0] in p1.keys() and d in p1[query[0]].keys():
                    d_score *= p1[query[0]][d]
                else:
                    d_score = 1
            else:
                if tuple[query[i - 1], query[i]] in bi_p2.keys() and query[i - 1] in p1.keys() and d in bi_p2[
                    tuple[query[i - 1], query[i]]].keys() and d in p1[query[i - 1]].keys():
                    d_score *= (bi_p2[tuple[query[i - 1], query[i]]][d]) / (p1[query[i - 1]][d])
                else:
                    d_score = 1

        dict_score_bi_gram[d] = d_score
    # 按照评分排序
    result = sorted(dict_score_bi_gram.items(), key=lambda x: x[1], reverse=True)
    return result


# 取前k高的

def topk(k, res):
    print("\nTop", k, "的结果如下：")
    top_k_res = {}
    for i in range(k):
        items = res[i]
        path = os.path.join("renamed", items[0])
        with open(path, mode='r', encoding='utf-8') as file:
            data = file.readlines()
            data = [line.strip() for line in data]
        print("第", i + 1, " : ", data[0], "  ", data[1], "\n", items[1])
        top_k_res[items[0]] = items[1]
    return top_k_res


# 查询函数

def uni_gram_search(query, lamadaa, k):
    print("\n uni-gram:")
    # 第一个式子计算结果 topK
    first_res = score_md_mc(query, lamadaa, c)
    print("\nfirst_score")
    first_top_k = topk(k, first_res)

    # 第二个式子计算结果 topK
    cal_pv_rv_cv(query, first_top_k)
    second_res = score_md_mc(query, lamadaa, cv)
    print("\nsecond_score")
    # second_top_k = topk(k, second_res)

    # 第三个式子计算结果 topK
    cal_pv1_rv1_cv1(query, first_top_k)
    third_res = score_md_mc(query, lamadaa, cv1)
    print("\nthird_score")
    # third_top_k = topk(k, third_res)

    # 初始LM公式计算结果 topK
    init_res = score_init_md_mc(query, lamadaa)
    print("\ninit_score")
    init_top_k = topk(k, init_res)

    # tf-idf作为权值计算结果 topK
    cal_tf_idf_prc()
    tf_idf_res = score_tf_idf_md_mc(query, lamadaa)
    print("\ntf_idf_score")
    # tf_idf_top_k = topk(k, tf_idf_res)
    # return first_res, second_res, third_res, init_res, tf_idf_res
    return init_res

def bi_gram_search(query, k):
    print("\n bi-gram:")
    bi_res = score_bi_gram(query)
    bi_gram_top_k = topk(k, bi_res)
    return bi_res


# 初始化
def init_all(lamada):
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    init_idf()
    cal_p_r_c()
    cal_pmc()
    cal_pmd()
    bi_gram()
    cal_p1_p2(lamada)


if __name__ == '__main__':
    lamada = 0.87
    top_k = 10
    init_all(lamada)
    # # print("dict_mc:", dict_mc)
    # # print("total_term:", total_term)
    # # print("dict_md:", dict_md)
    # # print("num_doc:", num_doc)
    # # print("total_doc:", total_doc)
    # q = ["奥运会", "篮球", "东京湾", "运动", "攀岩", "观众"]
    # res = score_rsv_mc(q, 0.8)
    # print("\n\n", res)
    # q = ["2022", "年", "北京", "冬奥会"]
    # query = "三人篮球参赛资格"
    # query = "2022年北京冬奥会"
    # query = "2023年乒乓球新加坡大满贯赛"
    # query = "查看以下赛事详情"
    query = "奥运参赛资格详细信息"

    q = doubleMax(query, 'ChineseDic.txt')
    print(q)
    # q = ["中国", "男子", "冰壶"]
    # res = score_rsv_mc(q, lamada)
    # print("score rsv mc")
    # topk(10, res)
    # res = score_bi_gram(q)
    # print("score bi-gram")
    # topk(10, res)
    uni_gram_search(q, lamada, top_k)
    bi_gram_search(q, top_k)
