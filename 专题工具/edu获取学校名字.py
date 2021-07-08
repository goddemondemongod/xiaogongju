import requests
import sys
import hashlib
from lxml import etree

def schoolname (url):  
    for i in range(1,100):
          pageurl = url + str(i)
          req = requests.get(pageurl) 
          tree = etree.HTML(req.text) 
          res = tree.xpath('//td[@class="am-text-center"]/a/text()')
          it=iter(res)
          for x in it:
           print("%s"%(x)) 
           with open("eduname.txt","a") as f:
               f.write("%s\n"%(x))



if __name__ == '__main__':
    schoolname('https://src.sjtu.edu.cn/rank/firm/?page=')
