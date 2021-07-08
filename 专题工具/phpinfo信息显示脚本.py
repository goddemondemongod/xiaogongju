import requests
import re

from bs4 import BeautifulSoup
# 自动分析phpinfo中的参数，显示其意义

class PHPINFO:
    def __init__(self,html):
        self.html = html
        self.html_tree = [] #元素类型为 <class 'bs4.element.Tag'>
        self.initBasicInfo()
        self.initImportantInfo()
        self.initExtInfo()
        self.VERSION = ['PHP版本']

    #初始化基本信息
    def initBasicInfo(self):
        SYSTEM = ['System','系统信息']
        EXT_DIR = ['extension_dir','php扩展的路径']
        REAL_IP = ["$_SERVER['HTTP_X_REAL_IP']",'真实IP']
        DOC_ROOT = ["$_SERVER['CONTEXT_DOCUMENT_ROOT']",'web根目录']
        TEMP_FILE = ['_FILES[','临时文件路径']
        self.BasicInfo = {'SYSTEM':SYSTEM,'EXT_DIR':EXT_DIR,'REAL_IP':REAL_IP,'DOC_ROOT':DOC_ROOT,'TEMP_FILE':TEMP_FILE}

    #初始化重要信息
    def initImportantInfo(self):
        allow_url_include = ['allow_url_include','远程文件包含']
        asp_tags = ['asp_tags','使用asp的标签解析']
        short_open_tag = ['short_open_tag','标签的问题，允许<??>这种形式，并且<?=等价于<? echo']
        disable_functions = ['disable_functions','禁用php执行系统命令的函数','黑名单绕过:pcntl是linux下的一个扩展，可以支持php的多线程操作,pcntl_exec函数的作用是在当前进程空间执行指定程序，版本要求：PHP > 4.2.0.:<?php pcntl_exec(“/bin/bash”, array(“/tmp/1.sh”));?>']
        enable_dl = ['enable_dl','利用扩展库绕过disable_functions，需要使用dl()并且开启这个选项']
        magic_quotes_gpc = ['magic_quotes_gpc','用来实现addslshes()和stripslashes()这两个功能的，对SQL注入进行防御']
        open_basedir = ['open_basedir','将用户可操作的文件限制在某目录下,但是这个限制是可以绕过的']
        self.ImpInfo = {'allow_url_include':allow_url_include,'asp_tags':asp_tags,'short_open_tag':short_open_tag,'disable_functions':disable_functions,'enable_dl':enable_dl,'magic_quotes_gpc':magic_quotes_gpc,'open_basedir':open_basedir}

    #初始化扩展信息
    def initExtInfo(self):
        session_upload_progress_name = ['session.upload_progress.name','当一个上传在处理中，同时POST一个与INI中设置的session.upload_progress.name同名变量时，当PHP检测到这种POST请求时，它会在$_SESSION中添加一组数据。所以可以通过Session Upload Progress来设置session']
        self.ExtInfo = {'session_upload_progress_name':session_upload_progress_name}

    #导入bs4进行分析
    def initSoup(self):
        self.soup = BeautifulSoup(self.html, 'lxml')
        soup = self.soup
        for tr in soup.find_all('tr'):
            self.html_tree.append(tr) #每一行

    #获取版本信息
    def getVersion(self):
        self.VERSION.append(self.html_tree[0].td.h1.string)
        print(self.VERSION)

    #取每一个键值对进行对比
    def compare_info(self):
        for tr in self.html_tree[1:]:
            # print('=========')
            # print(tr)
            (key,value) = self.get_key_value_from_tr(tr)
            # print((key,value))
            self.update_Info(self.BasicInfo,key,value)
            self.update_Info(self.ImpInfo, key, value)
            self.update_Info(self.ExtInfo, key, value)


    #更新数据
    def update_Info(self,info_dict,key,value):
        # print(key,value)
        for i in info_dict.keys():
            # print(info_dict[i][0])
            if info_dict[i][0] in key :
                info_dict[i].append(value)


    #获取每一行的key=value的数据
    def get_key_value_from_tr(self,tr):
        key_patt = r'<td class="e">(.+?)</td>'
        value_patt = r'<td class="v">(.+?)</td>'
        try:
            key = re.findall(key_patt,str(tr))[0]
            value = re.findall(value_patt,str(tr))[0]
        except:
            return ('NULL','NULL')
        return (key,value)

    #显示信息
    def echoInfo(self,info_dict,txt):
        print('====={}====='.format(txt))
        for key in info_dict.keys():
            print(info_dict[key])

    #入口主函数
    def start(self):
        self.initSoup()
        self.getVersion() #获取php版本
        self.compare_info() #获取数据
        self.echoInfo(self.BasicInfo, '基本信息')
        self.echoInfo(self.ImpInfo,'重要信息')
        self.echoInfo(self.ExtInfo,'额外信息')

# 下载phpinfo的html
def get_PHPINFO_html(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
        "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Upgrade-Insecure-Requests": "1"}
    response = session.get(url,headers=headers)
    return response.text #返回内容为字符串

if __name__ == '__main__':
    url = 'http://59.110.46.120:88/?mode=phpinfo'
    html = get_PHPINFO_html(url) #下载html
    myPHPINFO = PHPINFO(html) #实例
    myPHPINFO.start()