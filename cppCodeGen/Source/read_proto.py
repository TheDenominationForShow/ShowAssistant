import os
import re
from type_indentify import *

g_file_name = "sssss"
proto_path = r"xxxx\sss_proto\common"+"\\"+g_file_name+r".proto"

proto_content = None
include_list = []
def read_proto(proto_path):
    with open(proto_path,"r",encoding="utf-8") as f:
        proto_content = f.readlines()
    for item in proto_content:
        line_str = item[0:-1]
        if g_context.state == "start":
            if filter_line(line_str):
                continue
            rst = re.match(r"\s*{",line_str)
            if rst != None:
                g_context.state = "run"
                log.info(g_context.state)
        elif g_context.state == "empty" or g_context.state == "end":
            #解析出依赖头文件
            rst = re.match(r'import "common/\S\S*\.proto";',line_str)
            if rst != None	:
                parttern = re.compile(r'import "common/(\S\S*)\.proto";')
                m = parttern.match(line_str)
                include_list.append(m.group(1))
                log.info(m.group(1))
                continue
            if filter_line(line_str):
                continue
            if identify_massage(line_str):
                log.info(g_context.name)
                g_context.state = "start"
                continue
            if identify_enum(line_str):
                log.info(g_context.name)
                g_context.state = "start"
                continue
            if identify_data_member(line_str):
                continue
        elif g_context.state == "run":
            if filter_line(line_str):
                continue
            rst = re.match(r"\s*oneof\s*\w*{",line_str)
            if rst != None:
                g_context.extent["union"] = "Start"
                log.info(g_context.state)
                continue
            if identify_data_member(line_str):
                continue
            if identify_enum_member(line_str):
                continue
            rst = re.match(r"\s*}",line_str)
            if rst != None:
                #
                rt = g_context.extent.get("union")
                if rt != None:
                    g_context.extent["union"] = None
                else:
                    g_context.state = "end"
                    log.info(g_context.state)
    log.info("========================proto info=============================")
    message_len = 0
    enum_len = 0

    for  item in g_map:
        log.info("name = "+item +"    type="+g_map[item].meta)
        if g_map[item].meta != "ClassType":
            enum_len += 1
        else:
            message_len += 1
        #print(g_map[item].meta)
        '''
        for it in g_map[item].prop:
            ls = g_map[item].prop[it]
            print("	prop = "+it+ " len = "+str(len(ls)))
            for i in ls:
                #print("meta = "+ i.meta)
                #print("		name = " +i.name)
                pass
        '''
    log.info("map len = "+str(len(g_map)))
    log.info("enum_len = "+str(enum_len))
    log.info("message_len = "+str(message_len))
    log.info("========================proto info end=============================")

if __name__ =="__main__":
    pass