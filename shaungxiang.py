import os
from zhengxiang import leftMax
from nixiang import rightMax


def doubleMax(text, path):
    left = leftMax(path)
    right = rightMax(path)

    leftMatch = left.cut(text)
    rightMatch = right.cut(text)

    # 返回分词数较少者
    if (len(leftMatch) != len(rightMatch)):
        if (len(leftMatch) < len(rightMatch)):
            return leftMatch
        else:
            return rightMatch
    else:  # 若分词数量相同，进一步判断
        leftsingle = 0
        rightsingle = 0
        isEqual = True  # 用以标志结果是否相同
        for i in range(len(leftMatch)):
            if (leftMatch[i] != rightMatch[i]):
                isEqual = False
            # 统计单字数
            if (len(leftMatch[i]) == 1):
                leftsingle += 1
            if (len(rightMatch[i]) == 1):
                rightsingle += 1
        if (isEqual):
            return leftMatch
        if (leftsingle < rightsingle):
            return leftMatch
        else:
            return rightMatch


def main():
    path = "sepnews"
    i = 1
    list=os.listdir(path)
    list.sort();
    for dir in list:
        print(str(i))
        child_dir = os.path.join(path, dir)
        # print(child_dir)
        with open(child_dir, mode='r',encoding='utf-8') as file:
            data = file.readlines()
            data = [line.strip() for line in data]
        print(doubleMax(data[0], 'ChineseDic.txt'))
        print(doubleMax(data[1], 'ChineseDic.txt'))
        print('\n')
        i = i + 1