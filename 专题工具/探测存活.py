import  threading
import  time
import requests

with open('src.txt','r') as urls:
    urls1 = urls.readlines()
def fw(url):
    try:
        url = "http://"+i+"/"
        r = requests.get(url, timeout=1)
        if r.status_code == 200:
           print(url)
           with open('newsrc.txt','a') as f:
               f.write("{}\n".format(url))
        else:
            pass
    except:
        pass

for i in urls1:
     i = i.rstrip()
     i = str(i)
     t=threading.Thread(target=fw,args=(i,))
     t.start()
     #t.join()#原因必须上一个进程结束后才运行下一个进程,#如果不使用这个一秒钟即可打印完,常常跟daemon联合用

