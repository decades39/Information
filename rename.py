import os
import codecs

def ansitoutf8(filepath):
    #filepath='testindex'
    files=os.listdir(filepath)
    for file in files:
        file_name = filepath + '\\' + file
        f = codecs.open(file_name, 'r', 'ansi')
        ff = f.read()
        file_object = codecs.open(filepath + '\\' + file, 'w', 'utf-8')
        file_object.write(ff)


def renamefiles(oldpath,newpath):
    list=os.listdir(oldpath)
    list.sort();
    i=1;
    for dir in list:
        oldname = os.path.join(oldpath, dir)
        newname = os.path.join(newpath,str(i).zfill(3)+'.txt')
        os.rename(oldname, newname)
        i=i+1

path='testindex'
npath='renamed'
#ansitoutf8(path)
renamefiles(path,npath)