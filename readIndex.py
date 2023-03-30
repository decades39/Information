import os
import re
dict1 = {}
dict2 = {}

def readIndex(path):
    index = open(path, mode='r' ,encoding='utf-8')
    line = index.readline().strip()
    linenum=1
    while line:
        print(linenum)
        temp = re.split(' ---->|:', line)
        size = len(temp)
        dict1[temp[0]] = list()
        dict2[temp[0]] = temp[1]
        for i in range(size):
            if i > 1 & i%2==0:
                    txt = temp[i]
                    num = temp[i+1]
                    #print(' ',txt, ' ', num)
                    dict1[temp[0]].append([txt, num])
        line = index.readline().strip()
        linenum+=1
path=os.getcwd()+"\\IndexResult.txt"
readIndex(path)
# print(dict1)
for i in dict1.keys():
   print((i) + ': ' + str(dict2[i]) + '\n' + str(dict1[i]))



