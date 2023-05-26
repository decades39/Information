import os
from index import prune
from readIndex import progress, readIndex
import re
from McMd import init_all
from McMd import uni_gram_search
from McMd import bi_gram_search
from shaungxiang import doubleMax

def split_logic_expression(expression):

    # 去掉首尾多余的运算符
    while expression.startswith(('and', 'or', 'andnot')):
        expression = expression[3:].strip()
    while expression.endswith(('and', 'or', 'andnot')):
        expression = expression[:-3].strip()

    expression = expression.replace("(", "").replace(")", "")
    variables = []
    operators = []

    # 匹配中文字符、英文字母、数字
    pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]+', re.UNICODE)
    tokens = pattern.findall(expression)

    for token in tokens:
        if token.lower() in ('and', 'or', 'andnot'):  # 运算符
            operators.append(token.lower())
        else:  # 变量名
            variables.append(token)

    return variables, operators


def search_documents(query):
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    words, operators = split_logic_expression(query)
    result = []
    intermediate_result = []
    if len(words) > 0:
        if len(words) == 1 and len(operators) == 0:
            intermediate_result = progress("Onlyone", words)
        if len(operators) == 1 and len(words) == 2:
            if operators[0] == "and":
                intermediate_result = progress("And", words)
            if operators[0] == "or":
                intermediate_result = progress("Or", words)
            if operators[0] == "andnot":
                intermediate_result = progress("Not", words)
        elif len(operators) > 0 and all(x == 'and' for x in operators):
            intermediate_result = progress("MoreAnd", words)
        elif len(operators) > 0 and all(x == 'or' for x in operators):
            intermediate_result = progress("MoreOr", words)
        elif len(operators) > 1:
            intermediate_result = progress("More", words, operators)

    if len(intermediate_result) > 0:
        for item in intermediate_result:
            txt = item[0]  # 获取tuple中的Any元素
            path = os.path.join("renamed", txt)
            with open(path, mode='r', encoding='utf-8') as file:
                data = file.readlines()
                data = [line.strip() for line in data]
            # data[0] = prune(data[0])
            # data[1] = prune(data[1])
            result.append({'title': data[0], 'summary': data[1], 'url': txt, 'score': item[1]})
    return result


def search_unigram(query):
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    result = []
    intermediate_result = []
    q = doubleMax(query, 'ChineseDic.txt')
    print(q)
    intermediate_result = uni_gram_search(q, lamada, top_k)
    if len(intermediate_result) > 0:
        for item in intermediate_result:
            txt = item[0]  # 获取tuple中的Any元素
            path = os.path.join("renamed", txt)
            with open(path, mode='r', encoding='utf-8') as file:
                data = file.readlines()
                data = [line.strip() for line in data]
            # data[0] = prune(data[0])
            # data[1] = prune(data[1])
            result.append({'title': data[0], 'summary': data[1], 'url': txt, 'score': item[1]})
    return result

def search_bigram(query):
    path = os.getcwd() + "\\IndexResult.txt"
    readIndex(path)
    result = []
    intermediate_result = []
    q = doubleMax(query, 'ChineseDic.txt')
    print(q)
    intermediate_result = bi_gram_search(q, top_k)
    if len(intermediate_result) > 0:
        for item in intermediate_result:
            txt = item[0]  # 获取tuple中的Any元素
            path = os.path.join("renamed", txt)
            with open(path, mode='r', encoding='utf-8') as file:
                data = file.readlines()
                data = [line.strip() for line in data]
            # data[0] = prune(data[0])
            # data[1] = prune(data[1])
            result.append({'title': data[0], 'summary': data[1], 'url': txt, 'score': item[1]})
    return result

lamada = 0.87
top_k = 10
init_all(lamada)
# def main():
#     result = search_documents("还有 and 2020")
#     print("---------------------------------最终结果----------------------------------------------")
#     print(result)
#
#
# main()
