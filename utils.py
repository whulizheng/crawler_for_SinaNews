import json
import os


def readjson(address):
    with open(address, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def readtxt(address, limits=None):
    if limits is None:
        txt_tables = []
        f = open(address, "r")
        line = f.readline()  # 读取第一行
        while line:
            txt_data = str(line)
            txt_tables.append(txt_data.replace('\n', ''))  # 列表增加
            line = f.readline()  # 读取下一行
        return txt_tables
    else:
        count = 0
        txt_tables = []
        f = open(address, "r")
        line = f.readline()  # 读取第一行
        while line:
            if count == limits:
                break
            txt_data = str(line)
            txt_tables.append(txt_data.replace('\n', ''))  # 列表增加
            count += 1
            line = f.readline()  # 读取下一行
        return txt_tables


def scan_file(file_dir):
    files = []
    for roo, dirs, file in os.walk(file_dir):
        files.append(file)
    return files[0]


def save_news(data, title, text, path, default="unknown", illegal=["/", "\"", "\\", ":", "*", "<", ">", "|", "\t", "\n", "?"]):
    path = path+data+"\\"
    os.mkdir(path)
    text = "".join(text.split())
    files = scan_file(path)
    for i in illegal:
        title = title.replace(i, "")
    save_name = path+"erro.txt"
    if title == '':
        count = 0
        while default + "_"+str(count)+".txt" in files:
            count += 0
        save_name = path+default + "_"+str(count)+".txt"
        with open(save_name, 'w') as f:
            f.write(text)
    else:
        count = 0
        while default + "_"+str(count)+".txt" in files:
            count += 0
        if count == 0:
            save_name = path+title+".txt"
        else:
            save_name = path+title + "_"+str(count)+".txt"
        with open(save_name, 'w', encoding="utf-8") as f:
            f.write(text)
