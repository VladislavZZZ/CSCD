import os
path = r'C:\Users\Kizenkov_V\PycharmProjects\CSCD\lab_2_RSA-AES_CFB\server\data/'

def get_text(filename):
    text = ''
    with open(path + filename, 'r')as f:
        line = f.readline()
        while line:
            text += line
    return text

def get_file_list():
    list = ''
    tree = os.walk(path)
    for address, dirs, files in  tree:
        for file in files:
            list += file+'\n'
    return list[:-1]