#-*- coding:utf8 -*-
from __future__ import print_function
import os,re,logging
import copy
log = logging.getLogger(__name__)
class ConfParser():
    """
        配置文件解析类，用于生成配置文件对象
    用法：
        file：读取或者创建的配置文件路径
        ismake：在文件file不存在时，是否创建。默认为False
    """
    #配置全局通用conf_info属性
    init_info = {
                'ROOT':{
                    'status':True,
                    'parent':None,
                    'prefix':None,
                    'data':None,
                    'line_num':None
                    }
            }
    init_data = {'ROOT':{}}
    def __init__(self,conf_file,ismake=False):
        global conf_data,conf_info,current_info,current_data,current_path,conf_line,line_num
        self.status = {
                       'name':'confparser.ConfParser.__init__',
                       'result':True,
                       'comment':'',
                       'changes':{},
                       'data':{}
                       }
        #初始化
        self.init_conf(conf_file='NO')
        current_path = r"['ROOT']"
        current_data = eval('self.conf_data' + current_path)
        current_info = eval('self.conf_info' + current_path)
        line_num = 0
        self.conf_file = conf_file
        #生成文件对象
        try:
            if ismake:
                if not os.path.exists(os.path.dirname(self.conf_file)):
                    os.mkdir(os.path.dirname(self.conf_file))
                self.conf_file_obj = open(self.conf_file,'w')
            else:
                if os.path.exists(self.conf_file):
                    self.conf_file_obj = open(self.conf_file)
                    #调用readconf方法，读取配置文件
                    self.readconf(self.conf_file_obj)
                    #读取完毕后，关闭文件对象
                    self.conf_file_obj.close()
                else:
                    self.status['result'] = False
                    self.status['comment'] = '读取配置文件遇到错误,文件\"%s\"不存在！！！' % (self.conf_file)
                    log.error(self.status['comment'])
                    return
        except IOError as e:
            self.status['result'] = False
            self.status['comment'] = '读取配置文件遇到错误,信息如下：\nIOError: \n\t错误代码：%d\n\t错误类型：%s\n\t文件路径：%s\n' % (e.errno,e.strerror,e.filename)
            log.error(self.status['comment'])
            return        
    def init_conf(self,conf_file=None,op='r'):
        """
        用于初始化配置文件对象,创建配置文件对象
        用法：
        file：文件路径，默认为self.conf_file，为字符串
        op：文件对象模式，即open()方法的参数，为字符串
        """
        global conf_data,conf_info,current_info,current_data,current_path,conf_line,line_num
        #引用全局初始化属性
        self.conf_data = copy.deepcopy(ConfParser.init_data)
        self.conf_info = copy.deepcopy(ConfParser.init_info)
        self.conf_info['ROOT'].update({
                                        'name':'ROOT',
                                        #type可用的值为：section、key、list
                                        'type':'section'
                                       })
        current_path = r"['ROOT']"
        current_data = eval('self.conf_data' + current_path)
        current_info = eval('self.conf_info' + current_path)
        #创建文件对象
        if not conf_file == 'NO':
            if conf_file == None:
                conf_file = self.conf_file
            else:
                self.conf_file = conf_file
            try:
                self.conf_file_obj = open(file,op)
            except IOError as e:
                self.status['result'] = False
                self.status['comment'] = '读取配置文件内容遇到错误,信息如下:\nIOError: \n\t错误代码：%d\n\t错误类型：%s\n\t文件路径：%s\n' % (e.errno,e.strerror,e.filename)
                log.error(self.status['comment'])
                return          
    def add_section(self,name,prefix=None,section_type='section',last_eof='{',status=False):
        global conf_data,conf_info,current_info,current_data,current_path,conf_line,line_num
        if section_type == 'list':
            data = []
        else:
            data = {}
        #判断字段名是否已经存在
        if type(current_data) == list:
            self.status['result'] = False
            self.status['comment'] = ('配置文件%s配置错误:列表内不可进行嵌套其他配置段，只能包含列表数据，信息如下:\n\t行号:%s\n\t内容:%s\n' % (self.conf_file,line_num,conf_line))
            return self.status
        else:
            if not name in current_data.keys():
                current_data[name] = data
                #更新数据至conf_data
                exec('self.conf_data' + current_path + '.update(current_data)')
    
                #依据闭合情况，配置当前级别状态信息
                if 'name' in current_info.keys():
                    parent = current_info['name']
                else:
                    parent = 'None'
                current_info[name] = {
                    'status':status,
                    'parent':parent,
                    'prefix':prefix,
                    'name':name,
                    'type':section_type,
                    'data':conf_line,
                    'line_num':line_num
                    }
                #提交当前级别状态信息
                exec('self.conf_info' + current_path + '.update(current_info)')
                #更新conf_current信息
                current_path = '%s[\'%s\']' % (current_path,name)
                current_data = eval('self.conf_data' + current_path)
                current_info = eval('self.conf_info' + current_path)
            else:
                if current_info[name]['type'] == 'key':
                    current_path = '%s[\'%s\']' % (current_path,name)
                    current_data = eval('self.conf_data' + current_path)
                    current_info = eval('self.conf_info' + current_path)
                else:
                    self.status['result'] = False
                    self.status['comment'] = '读取配置文件遇到错误: 配置节%s重复，请检查！！\n内容：%s' % (name,conf_line)
                    log.error(self.status['comment'])
                    return self.status


    def list_to_str(self,conflist):
        """
        转换参数列表为字符串
        用法：
        list：参数列表，为列表
        """
        conf = ''
        for l in conflist:
            conf = conf + ' ' + l
        return conf.strip()
    
    def readconf(self,conf_file=None):
        """
        用于读取配置文件，生成conf_data和conf_info字典，存储配置信息
        用法：
        file：配置文件对象，文件类型
        """
        global current_data,conf_line,current_path,current_info,conf_data,conf_info,line_num
        if conf_file == None:
            conf_file= self.conf_file_obj
        for conf_line in conf_file:
            line_num += 1
            if re.match(r'^[\s]*$',conf_line) or re.match(r'^[ \t]*#.*',conf_line):
                continue
            #匹配 tomcat {
            elif re.match(r'^[ \t]*[a-zA-Z_]+[\w\-]*[ \t]*[\{]{1}[\s]*$',conf_line):
                #section名称
                self.add_section(name=conf_line.split()[0])
            #匹配     path = /apps/zebrawms/zebrawms_1
            elif re.match(r'^[ \t]*[a-zA-Z_]+[\w\-]*[ \t]+[=]{1}[ \t]+[^\r\n\f\v\{\}]+([ \t]*|\S*)$',conf_line):
                #数据检测
                if not type(current_data) == dict:
                    self.status['result'] = False
                    self.status['comment'] = '配置错误：\"列表\"类型配置段不能包含非\"列表\"类型配置行  \n\t文件: %s \n\t配置段类型: %s \n\t配置行行号: %d \n\t配置行内容：%s' % (self.conf_file,current_info['type'],line_num,conf_line)
                    log.error(self.status['comment'])
                    return self.status
                #section名称
                section = conf_line.split()[0]
                #增加当前级别的数据
                current_data[section] = self.list_to_str(conf_line.split()[2:])
            #匹配                }    
            elif re.match(r'^[ \t]*[\}]{1}[ \t]*$',conf_line):
                #更新数据至conf_data
                if current_info['type'] == 'list':
                    exec('self.conf_data' + current_path + ' = current_data')
                else:
                    exec('self.conf_data' + current_path + '.update(current_data)')

                #依据闭合情况，配置当前级别状态
                current_info['status'] = True
                #提交当前级别状态信息
                exec('self.conf_info' + current_path + '.update(current_info)')

                #更新conf_current信息
                current_path = current_path[:-len('[\'' + current_info['name'] + '\']')]
                current_data = eval('self.conf_data' + current_path)
                current_info = eval('self.conf_info' + current_path)
                if 'type' in current_info:
                    if current_info['type'] == 'key' and current_info['status']:
                        current_path = current_path[:-len('[\'' + current_info['name'] + '\']')]
                        current_data = eval('self.conf_data' + current_path)
                        current_info = eval('self.conf_info' + current_path)
                else:
                    self.status['result'] = False
                    self.status['comment'] = '读取配置文件错误: \n\t配置信息错误：关键字为\"%s\"的配置段\"%s\"重复了!! \n\t错误配置内容: %s\n\t位于文件%s第%d行' % (current_info['name'],current_info['parent'],conf_line,self.conf_file,line_num)
                    log.error(self.status['comment'])
                    return self.status
            #匹配    wmsWeb = {
            elif re.match(r'^[ \t]*[a-zA-Z_]+[\w\-]*[ \t]+[=]{1}[ \t]+[\{]{1}[\s]*$',conf_line):
                self.add_section(name=conf_line.split()[0],section_type='list')
            #匹配    version 1.0.0 = {
            elif re.match(r'^[ \t]*[a-zA-Z_]+[\w\-]*[ \t]+[\w\-\.]*[ \t]+[=]{1}[ \t]+[\{]{1}[\s]*$',conf_line):
                #关键字处理
                self.add_section(name=conf_line.split()[0],section_type='key',status=True)
                #列表
                self.add_section(name=conf_line.split()[1],prefix=conf_line.split()[0],section_type='list')
            #匹配    instence zebrawms_1 {
            elif re.match(r'^[ \t]*[a-zA-Z_]+[\w\-]*[ \t]+[\w\-\.\/]*[ \t]+[\{]{1}[\s]*$',conf_line):
                #关键字处理
                self.add_section(name=conf_line.split()[0],section_type='key',status=True)
                #参数处理
                self.add_section(name=conf_line.split()[1],prefix=conf_line.split()[0])
            #匹配    web_1,    或者    web_2
            elif re.match(r'^[ \t]*[^\r\n\f\v\{\}]+[ \t]*[\,]?[\s]*$',conf_line):
                #数据检测
                if not type(current_data) == list:
                    self.status['result'] = False
                    self.status['comment'] = '配置错误："列表"类型的配置行,必须包含在以\"= {\"结尾的配置段内  \n\t文件: %s \n\t配置段类型: %s \n\t配置行行号: %d \n\t配置行内容：%s' % (self.conf_file,current_info['type'],line_num,conf_line)
                    log.error(self.status['comment'])
                    return self.status
                #增加当前级别的数据
                current_data.append(conf_line.strip().split(',')[0])
            else:
                self.status['result'] = False
                self.status['comment'] = '读取配置文件错误: \n\t配置信息错误：该行内容没有匹配到任何规则!! \n\t错误配置内容: %s\n\t位于文件%s第%d行' % (conf_line,self.conf_file,line_num)
                log.error(self.status['comment'])
                return self.status
            
    def write_conf(self,conf_file=None,conf_data=None,conf_info=None):
        """
        分析配置文件数据及信息，并将配置数据写入文件中，实现配置配置文件的编写功能
        用法：
        file：写入的配置文件对象，文件
        conf_data：配置文件数据字典，字典
        conf_info：配置文件信息字典，字典
        """   
        def dict_parser(conf_file=None,conf_data=None,conf_info=None,key=None):
            global level
            
            if conf_info['type'] == 'section':
                line = '\t' * level + key + ' {' + '\n'
                conf_file.write(line)
                parser(conf_file,conf_data,conf_info)
            elif conf_info['type'] == 'key':
                for k in conf_data.keys():
                    line = '\t' * level + key + ' ' + k + ' {' + '\n'
                    conf_file.write(line)
                    if type(conf_data[k]) == dict:
                        parser(conf_file,conf_data[k],conf_info[k])
                    else:
                        list_parser(conf_file,conf_data[k],conf_info[k],key=k)
        def list_parser(conf_file=None,conf_data=None,conf_info=None,key=None):
            global level
            line = '\t' * level + key + ' = {' + '\n'
            conf_file.write(line)
            for k in conf_data[:len(conf_data)-1]:
                line = '\t' * (level + 1) + k + ',' + '\n'
                conf_file.write(line)
            else:
                line = '\t' * (level + 1) + str(conf_data[-1:][0]) + '\n'
                conf_file.write(line)
            line = '\t' * level + '}' + '\n'
            conf_file.write(line)     
        def str_parser(conf_file=None,conf_data=None,key=None):
            global level
            line = '\t' * level + key + ' = ' + conf_data + '\n'
            conf_file.write(line)
            
        def parser(conf_file=None,conf_data=None,conf_info=None):
            global level
            try:
                level += 1
            except NameError:
                level = 0
            #判断是否key对应的value的类型，依据不同类型进行不同的处理
            for key in conf_data.keys():
                #为字典时的操作
                if type(conf_data[key]) == dict:
                    dict_parser(conf_file,conf_data[key],conf_info[key],key=key)
                #为列表时的操作
                elif type(conf_data[key]) == list:
                    list_parser(conf_file,conf_data[key],conf_info[key],key=key)
                #为字符串时的操作
                elif type(conf_data[key]) == str:
                    str_parser(conf_file,conf_data[key],key=key)
            level -= 1 
            #判断当字典处理完成后，不在结尾写入多余的'}'符号
            if not conf_info['name'] == 'ROOT':
                line = '\t' * level + '}' + '\n'
                conf_file.write(line)
        #初始化配置信息
        if conf_file== None:
            conf_file= self.conf_file_obj
        if conf_data == None:
            conf_data = self.conf_data
        if conf_info == None:
            conf_info = self.conf_info
        try:
            #开始分析字典
            parser(conf_file,conf_data,conf_info)
        except IOError as e:
            self.status['result'] = False
            self.status['comment'] = '读取配置文件遇到错误: \nIOError: \n\t错误代码：%d\n\t错误类型：%s\n\t文件路径：%s\n' % (e.errno,e.strerror,e.filename)
            log.error(self.status['comment'])
            return self.status
        
        except KeyError as e:
            self.status['result'] = False
            self.status['comment'] = '读取配置文件遇到错误: \nKeyError: \n\tKey：%s\n\tconf_data: %s\n\tconf_info: \n\t' % (e.args,parser.conf_data[e.args],parser.conf_info[e.args])
            log.error(self.status['comment'])
            return self.status
        
    def eof_check(self,conf_info=None):
        """
        用于检查配置文件配置语法
        用法：
        conf_info：读取配置文件后，生成的conf_info字典，字典
        """
        #初始conf_info信息
        if conf_info == None:
            conf_info = self.conf_info['ROOT']
        else:
            if not type(conf_info) == dict:
                self.status['result'] = False
                self.status['comment'] = '执行配置文件eof检查出现错误,信息：参数conf_info类型必须为字典！'
                log.error(self.status['comment'])
                return self.status
        if conf_info['status']:
            for key in conf_info.keys():
                current_info = conf_info[key]
                if type(current_info) == dict:
                    self.eof_check(current_info)
        else:
            self.status['result'] = False
            self.status['comment'] = '配置文件eof检查出现错误：\n配置错误：配置段没有闭合！！\n位于文件\"%s\"第%d行\n配置行内容：%s' % (self.conf_file,conf_info['line_num'],conf_info['data'])
            log.error(self.status['comment'])
            return self.status
            
    def tmpl_check(self,tmpl,conf_info=None):

        if conf_info == None:
            conf_info = self.conf_info
        else:
            for d in [tmpl,conf_info]:
                if not type(d) == dict:
                    self.status['result'] = False
                    self.status['comment'] = '执行配置文件模版匹配检查出现错误: 参数%s类型必须为字典！' % (d)
                    log.error(self.status['comment'])
                    return self.status
        if tmpl.keys() == conf_info.keys():
            for key in tmpl.keys():
                if type(tmpl[key]) == dict:
                    self.tmpl_check(tmpl[key],conf_info[key])
        else:
            error_list = [ x for x in tmpl.keys() if not x in conf_info.keys()]
            log.error(error_list)
            self.status['result'] = False
            self.status['comment'] = '执行配置文件模版匹配检查出现错误：缺少配置字段\"%s\",位于文件\"%s\"' % (str(error_list),self.conf_file)
            log.error(self.status['comment'])
            return self.status


######################################################################################################
#模块函数
def reduce_conf_info(conf_info):
    """
    精简conf_info字典,返回一个每个级别仅包含name和type KEY的字典
    用法：
    conf_info：配置文件信息字典，字典
    """
    for key in list(conf_info.keys()):
        if (not key in  ConfParser.init_info['ROOT'].keys()) and type(conf_info[key]) == dict:
            conf_info[key] = reduce_conf_info(conf_info[key])
        else:
            for k in [x for x in ConfParser.init_info['ROOT'].keys() if x in conf_info.keys()]:
                conf_info.pop(k)
    return conf_info
