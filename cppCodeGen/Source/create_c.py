from read_proto import *
from create_c_str import *

cpp_filename = r"xxxxxx\TSDB\source\common"+ "\\" + g_file_name

# model public

#========================================cpp==================================
def create_c(cpp_filename,file_name):
    print(cpp_filename)
    c_content_new = []
    c_content_new.append(c_content_1_str.format(FileName = file_name ))
    c_content_new += c_content_2_str_list
    for item in g_map:
        if g_map[item].meta != "ClassType":
            continue
        c_content_new.append(c_content_3_str.format(ClassName=g_map[item].name))
        #默认构造
        c_content_new.append(c_content_4_str.format(ClassName=g_map[item].name))
        for it in g_map[item].prop["data_member"]:
            #print(h_header_7_str.format(VarType = it.prop["SubType"],VarName = it.name))
            if it.prop["type"] == "Array":
                c_content_new.append(c_content_5_str.format(VarName = it.name))
                log.info(it.name)
            elif it.prop["type"] == "map":
                c_content_new.append(c_content_5_str.format(VarName = it.name))
            else:
                SubType = it.prop["SubType"]
                Type = ""
                if isBase(SubType):
                    SubType += "_t"
                    c_content_new.append(c_content_6_str.format(VarName = it.name,CtorParam = ""))
                elif isString(SubType):
                    SubType = "CString"

                    log.info("ctor begin"+it.name)
                    log.info(it.prop)
                    c_content_new.append(c_content_5_str.format(VarName = it.name))
                    log.info("ctor end"+it.name)
                elif is_google_protobuf(SubType) :
                    #print("is_google_protobuf = "+SubType)
                    if "google.protobuf.Empty" == SubType:
                        continue
                    if "google.protobuf.Timestamp" == SubType:
                        SubType = "CTimestamp"
                        c_content_new.append(c_content_6_str.format(VarName = it.name,CtorParam = ""))
                elif isEnum(SubType):
                    c_content_new.append(c_content_6_str.format(VarName = it.name,CtorParam = ""))
                    pass
                elif "Variant" == SubType :
                    #print("catch Variant classname = " + item)
                    SubType = "ns_datatype::Variant"
                    c_content_new.append(c_content_5_str.format(VarName = it.name))
                elif is_def_class(SubType):
                    pass
                    c_content_new.append(c_content_5_str.format(VarName = it.name))
                else:
                    SubType = it.prop["SubType"]+"Ptr"
                    c_content_new.append(c_content_6_str.format(VarName = it.name,CtorParam = "nullptr"))
        c_content_new.append(c_content_7_str)
        # operator=
        c_content_new.append(c_content_8_str.format(ClassName=g_map[item].name))
        for it in g_map[item].prop["data_member"]:
            #print(h_header_7_str.format(VarType = it.prop["SubType"],VarName = it.name))
            if it.prop["type"] != "map":
                if "google.protobuf.Empty" == it.prop["SubType"]:
                    continue
            c_content_new.append(c_content_9_str.format(VarName = it.name))
        c_content_new.append(c_content_10_str)
        c_content_new.append(c_content_11_str.format(ClassName=item))

        # serialize
        c_content_new.append(c_content_12_str.format(ClassName=item))
        for it in g_map[item].prop["data_member"]:
            #print(h_header_7_str.format(VarType = it.prop["SubType"],VarName = it.name))
            if it.prop["type"] == "map":
                continue
            SubType = it.prop["SubType"]
            if it.prop["type"] == "Array":
                if isEnum(SubType):
                    c_content_new.append(c_content_17_str.format(VarName = it.name, VarType = SubType))
                elif isBase(SubType):
                    SubType += "_t"
                    c_content_new.append(c_content_17_str.format(VarName = it.name, VarType = SubType))
                else:
                    c_content_new.append(c_content_14_str.format(VarName = it.name))
                continue
            Type = ""
            log.info(it.prop)
            if isBase(SubType):
                SubType += "_t"
                c_content_new.append(c_content_13_str.format(VarName = it.name))
            elif isString(SubType):
                SubType = "CString"
                c_content_new.append(c_content_13_str.format(VarName = it.name))
            elif is_google_protobuf(SubType) :
                #print("is_google_protobuf = "+SubType)
                if "google.protobuf.Empty" == SubType:
                    continue
                if "google.protobuf.Timestamp" == SubType:
                    SubType = "CTimestamp"
                    c_content_new.append(c_content_13_str.format(VarName = it.name))
            elif isEnum(SubType):
                c_content_new.append(c_content_13_str.format(VarName = it.name))
                pass
            elif "Variant" == SubType :
                #print("catch Variant classname = " + item)
                SubType = "ns_datatype::Variant"
                c_content_new.append(c_content_13_str.format(VarName = it.name))
            elif is_def_class(SubType):
                c_content_new.append(c_content_13_str.format(VarName = it.name))
            else:
                SubType = it.prop["SubType"]+"Ptr"
                #c_content_new.append(c_content_14_str.format(VarName = it.name))
                c_content_new.append(c_content_18_str.format(VarName = it.name,VarType = it.prop["SubType"]))
                
        c_content_new.append(c_content_15_str)

    c_content_new.append(c_content_16_str)

    with open(cpp_filename+".cpp","w") as f:
        f.writelines(c_content_new)