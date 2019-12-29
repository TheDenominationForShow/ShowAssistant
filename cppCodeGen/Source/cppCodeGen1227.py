import os
import re

'''
现在只关心类，不考虑模板、类内类定义和枚举union等来实践一下
模型大概是.h和.cpp
并且不考虑异常排版
'''
# 过滤行
def filter_line(line_str):
    while True:
        rst = re.match(r"\s*//",line_str)
        if rst != None:
            break
        if len(line_str.split(" ")):
            pass
        rst = re.match(r"\s*{",line_str)
        if rst != None:
            break
        rst = re.match(r"\s*}",line_str)
        if rst != None:
            break
# 识别类
def identify_class(line_str):
    rst = re.match(r"class[ \t].*",line_str)
    if rst == None:
        return False
    #获取类名
    words = line_str.split(" ")
    for i in range(0,len(words)):
        rst = re.search(":",words[i])
        if rst != None:
            break
        class_name = words[i]
    return True

#识别方法
def identify_func_member(line_str):
    rst = re.match(r".*[ \t\:](\S\S*)[ \t]*\(.*\)",line_str)
    if rst == None:
        return False
    #获取函数名
    pattern = re.compile(r".*[ \t\:](\S\S*)[ \t]*\(.*\)")
    m = pattern.match(line_str)
    if m != None:
        func_name = m.group(1)
    return True
    
#识别数据成员
def identify_data_member(line_str):
    rst = re.match(r"\s*\w*[ \t]*\w*[ \t]*;",line_str)
    if rst == None:
        return False
    pattern = re.compile(r"[\w]\w*")
    words = m.findall(item)
    for word in words:
        print(word)
    return True


