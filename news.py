import os

#将总的txt文件分别存储为每条资讯，txt内以标题为名字，内存标题和简介，保存在sepnews文件夹中
def sepfile(txtname,data):
    pwd = os.getcwd()
    folder=pwd+"\sepnews\\"
    name=folder+txtname+'.txt'
    if not os.path.exists(name):
        f = open(name, mode='w', encoding='utf-8')
        f.close()
    f=open(name,mode='a+',encoding='utf-8')
    f.write(data+'\n')
    f.close()


#读取整的txt，以空行为分割将每条资讯存为单独的文件
def files(filename):
    f=open(filename,encoding='UTF-8')
    line=f.readline().strip()
    txt=[]
    txt.append(line)
    while line:
        line = f.readline()
        #过滤掉由于巴黎奥运会图标复制导致的一行
        if line in ['2024年巴黎奥运会\n']:
            continue
        if line in ['\n','\r\n']:
            lentxt=len(txt)
            for i in range(lentxt):
                print(txt[i]+' ')
                #sepfile(txt[0],txt[i])
            print("--------------------------")
            txt=[]
            #print("line*********"+line)
        else:
            line=line.strip()
            txt.append(line)
            #print("line*********"+line)
    lentxt=len(txt)
    for i in range(lentxt):
         print(txt[i]+' ')
         #sepfile(txt[0], txt[i])

#处理整文件
files('新闻.txt')