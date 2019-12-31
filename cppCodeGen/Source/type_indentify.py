import os
import re
import logging

log = logging.getLogger("fuck")
file_handler = logging.FileHandler(filename="fuck.log",encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s -[%(filename)s:%(lineno)d]")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.setLevel(logging.INFO)

class Word_Meta():
	def __init__(self):
		self.meta = None
		self.name = None
		self.prop = {}

class Contex(Word_Meta):
	def __init__(self):
		super().__init__()
		self.state = "empty"# "empty" "start" "run" "end"
		self.extent = {} # "dtor" 

g_context = Contex()
g_map = {}
def filter_line(line_str):
	ret = True
	while True:
		rst = re.match(r"\s*//",line_str)
		if rst != None:
			break
		if len(line_str.split(" ")) < 2  and line_str.split(" ")[0]=="\n":
			break
		'''
		rst = re.match(r"\s*{",line_str)
		if rst != None:
			break
		rst = re.match(r"\s*}",line_str)
		if rst != None:
			break
		'''
		ret = False
		break
	return ret
def identify_enum(line_str):
	rst = re.match(r"[ \t]*enum[ \t].*",line_str)
	if rst == None:
		return False
		#提取名称
	pattern = re.compile(r"[ \t]*enum[ \t]*(\w\w*)")
	e = pattern.match(line_str)
	if e != None:
		log.info("ENUM == "+e.group(1))
	meta = Word_Meta()
	meta.meta = "EnumType"
	meta.name = e.group(1)
	meta.prop = {}
	meta.prop["enum_member"] = []
	g_map[meta.name] = meta
	g_context.meta = "EnumType"
	g_context.name = meta.name
	return True

def identify_enum_member(line_str):
	rst = re.match(r"[ \t]*\w\w*[ \t]*\=[ \t]*\w\w*[ \t]*;",line_str)
	if rst == None:
		return False
	#print(line_str)
	meta  = g_map[g_context.name]
	meta.prop["enum_member"].append(line_str)
	return True
def identify_massage(line_str):
	rst = re.match(r"[ \t]*message[ \t].*",line_str)
	if rst == None:
		log.info(line_str)
		return False
	'''
	words = line_str.split(" ")
	for i in range(0,len(words)):
		rst = re.search(":",words[i])
		if rst != None:
			break
		class_name = words[i]
	'''
	pattern = re.compile(r"[ \t]*message[ \t][ \t]*(\w\w*)")
	e = pattern.match(line_str)
	if e != None:
		class_name = e.group(1)
	log.info(class_name)
	g_context.meta = "ClassType"
	g_context.name = class_name
	meta = Word_Meta()
	meta.meta = "ClassType"
	meta.name = class_name
	meta.prop = {}
	meta.prop["data_member"] = []
	meta.prop["union_member"] = []
	g_map[g_context.name] = meta
	return True

def identify_data_member(line_str):
	rst = re.match(r".*\w[\w\<\>]*[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;",line_str)
	if rst == None:
		return False
	meta = Word_Meta()
	meta.meta = "Variant"
	meta.prop = {}
	meta.prop["type"] = None
	meta.prop["SubType"] = None
	meta.prop["class"] = g_context.name
	#提取名称
	pattern = re.compile(r".*[ \t][ \t]*(\w\w*)[ \t]*\=[ \t]*\d\d*[ \t]*;")
	e = pattern.match(line_str)
	if e != None:
		#print("identify_data_member   " +e.group(1))
		meta.name = e.group(1)
		#处理变量名为关键字的情况
		if meta.name == "operator":
			meta.name = "operatorType"
		elif meta.name == "case":
			meta.name = "caseVar"
		elif meta.name == "version":
			meta.name = "versionVar"
	#提取类型
	while True:
		#匹配array
		rst = re.match(r"\s*repeated[ \t][ \t]*\S\S*[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;",line_str)
		if rst != None:
			#print("None == "+line_str)
			pattern = re.compile(r"\s*repeated[ \t][ \t]*(\S\S*)[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;")
			e = pattern.match(line_str)
			if e != None:
				meta.prop["type"] = "Array"
				meta.prop["SubType"] =e.group(1)
				meta.name += "s"
				break
			#print("Y == "+line_str)
        
        #匹配map map<string, Variant>
		rst = re.match(r"[ \t]*map\<[ \t]*\S\S*[ \t]*,[ \t]*\S\S*[ \t]*\>[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;", line_str)
		if  rst != None:
			meta.prop["type"] = "map"
			pattern = re.compile(r"[ \t]*map\<[ \t]*(\S\S*)[ \t]*,[ \t]*\S\S*[ \t]*\>[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;")
			e = pattern.match(line_str)
			if e != None:
				name = e.group(1)
				if e.group(1) == "bytes":
					name = "CBlob"
				meta.prop["key"] = name
			pattern = re.compile(r"[ \t]*map\<[ \t]*\S\S*[ \t]*,[ \t]*(\S\S*)[ \t]*\>[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;")
			e = pattern.match(line_str)
			if e != None:
				name = e.group(1)
				if e.group(1) == "bytes":
					name = "CBlob"
				meta.prop["value"] = name	
			break
		#匹配普通变量
		pattern = re.compile(r"[ \t]*(\S\S*)[ \t][ \t]*\w\w*[ \t]*\=[ \t]*\d\d*[ \t]*;")
		e = pattern.match(line_str)
		if e != None:
			name = e.group(1)
			if e.group(1) == "bytes":
				name = "CBlob"
			meta.prop["type"] = name
			meta.prop["SubType"] =name
			break
		break
	if g_context.meta == "ClassType":
		rt = g_context.extent.get("union")
		if rt != None:
			log.info("union_member "+meta.name)
			g_map[g_context.name].prop["union_member"].append(meta)
		else:
			g_map[g_context.name].prop["data_member"].append(meta)
	return True

base_type_list =["bool","short","byte","int","long","float","double","long"]
string_type_list = ["string"]
container_type = []

def isBase(var_type):
    ret = False
    for target in base_type_list:
        rst = re.match(target+r"\w*",var_type)
        if rst != None:
            ret = True
            break
    return ret
def isString(var_type):
	ret = False
	for target in string_type_list:
		rst = re.match(target+r"\w*",var_type)
		if rst != None:
			ret = True
			break
	return ret

def is_google_protobuf(var_type):
	ret = False
	rst = re.match(r"google\.protobuf\.\w\w*",var_type)
	if rst != None:
		ret = True
	return ret
def isEnum(var_type):
	ret = False
	for item in g_map:
		if g_map[item].meta == "EnumType":
			if var_type == g_map[item].name:
				ret = True
				break
	rst = re.match(r"Enum\w\w*",var_type)
	if rst != None:
		#print("isEnum = " +var_type)
		ret = True
	#特化在其他头文件中，不是Enum开头的枚举
	if "sdkfjlajdf" == var_type:
		ret = True
	elif "xxxxx" == var_type:
		ret = True
	return ret
def is_def_class(var_type):
	ret = False
	if var_type == "xxxxxx":
		ret = True
	return ret