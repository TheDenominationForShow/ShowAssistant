from create_h import *
from create_c import *

if __name__ =="__main__":
    print("hello")
    rst = os.listdir(r"zzzz_proto\common")
    print(rst)
    for item in rst:
        if "datatype" == item:
            continue
        print("正在处理----"+item)
        g_context.name = None
        g_context.prop.clear()
        g_context.state = "empty"
        g_map.clear()
        name,ext = os.path.splitext(item)
        print(name)
        g_file_name = name
        proto_path = r"zzzzzzproto\common"+"\\"+g_file_name+r".proto"
        proto_content = None
        include_list.clear()
        header_filename = r"zzzzz\include\common" +"\\"+g_file_name+".h"
        cpp_filename = r"xxxxxx\source\common"+ "\\" + g_file_name
        print(cpp_filename)

        read_proto(proto_path)
        create_h(header_filename,g_file_name)
        create_c(cpp_filename,g_file_name)
