from read_proto import *
from create_h_str import *
header_filename = r"xxxx\include\common" +"\\"+g_file_name+".h"

def convert_type(SubType):
    if isBase(SubType):
        SubType += "_t"
    elif isString(SubType):
        SubType = "CString"
    elif is_google_protobuf(SubType) :
        #print("is_google_protobuf = "+SubType)
        if "google.protobuf.Empty" == SubType:
            pass
        elif "google.protobuf.Timestamp" == SubType:
            SubType = "CTimeStamp"
        elif "google.protobuf.Any" == SubType:
            SubType = "xxxxxPtr"
    elif isEnum(SubType):
        pass
    elif "Variant" == SubType :
        #print("catch Variant classname = " xx+ item)
        SubType = "xxxxxxe::Variant"
    elif is_def_class(SubType):
        pass
    else:
        SubType = SubType+"Ptr"
    return SubType

def create_h(header_filename,file_name):
    print(header_filename)
    h_content_new = []

    h_content_new.append(h_header_1_str.format(FileName = file_name))
    for item in include_list:
        h_content_new.append(h_header_2_str.format(Path =item))
    if file_name == "config_public":
        h_content_new.append(h_header_2_str.format(Path ="runtime"))
    if "system_unit" == file_name:
        h_content_new.append(r'#include "base/base_inc.h"')
    else:
        h_content_new.append(h_header_3_str)
    h_content_new.append(h_header_4_str)
    #枚举
    for item in g_map:
        if g_map[item].meta != "EnumType":
            continue
        h_content_new.append("enum "+g_map[item].name+"\n")
        h_content_new.append("{\n")
        for it in g_map[item].prop["enum_member"]:
            h_content_new.append(it.replace(";",",")+"\n")
        h_content_new.append("};\n")


    # 类
    for item in g_map:
        if g_map[item].meta != "ClassType":
            continue
        h_content_new.append(h_header_12_str.format(ClassName=g_map[item].name))
    for item in g_map:
        if g_map[item].meta != "ClassType":
            continue
        h_content_new.append(h_header_6_str.format(ClassName=g_map[item].name))

        for it in g_map[item].prop["data_member"]:
            #print(h_header_7_str.format(VarType = it.prop["SubType"],VarName = it.name))
            if it.prop["type"] == "map":
                map_format_str = '''
    struct compare
	{{
		bool operator() (const CString& lstr, const CString& rstr)const {{ return (lstr.compare(rstr) < 0) ? true : false;}};
	}};
    ns_base::xxxlMap<{key}, {value},compare> {VarName};
                '''
                Type = map_format_str.format(key = convert_type(it.prop["key"]), value = convert_type(it.prop["value"]),VarName = it.name)
                #h_content_new.append(h_header_7_str.format(VarType = Type,VarName = it.name))
                h_content_new.append(map_format_str.format(key = convert_type(it.prop["key"]), value = convert_type(it.prop["value"]),VarName = it.name))
                continue    
            log.info(it.prop["type"])           
            SubType = it.prop["SubType"]
            if "google.protobuf.Empty" == SubType:
                continue
            if it.prop["type"] == "Array":
                Type = "Array<"+convert_type(SubType)+">"
            else:
                Type = convert_type(SubType)
            h_content_new.append(h_header_7_str.format(VarType = Type,VarName = it.name))
        if len(g_map[item].prop["union_member"]) == 0:
            #print(len(g_map[item].prop["union_member"]))
            h_content_new.append(h_header_11_str.format(ClassName=g_map[item].name))
            continue
        h_content_new.append(h_header_8_str)
        for it in g_map[item].prop["union_member"]:
            #print(h_header_9_str.format(VarType = it.prop["SubType"],VarName = it.name))
            if it.prop["type"] == "map":
                map_format_str = "  xxxxMap<{key}, {value}> xxxxp;"
                Type = map_format_str.format(key = it.prop["key"], value = it.prop["value"])
                continue 
            SubType = it.prop["SubType"]
            Type = ""
            SubType = it.prop["SubType"]
            if "google.protobuf.Empty" == SubType:
                continue
            if it.prop["type"] == "Array":
                Type = "Array<"+convert_type(SubType)+">"
            else:
                Type = convert_type(SubType)
            h_content_new.append(h_header_9_str.format(VarType = Type,VarName = it.name))
        h_content_new.append(h_header_10_str)
        h_content_new.append(h_header_11_str.format(ClassName=g_map[item].name))
    h_content_new.append(h_header_5_str.format(FileName = file_name))
    with open(header_filename,"w") as f:
        f.writelines(h_content_new)
