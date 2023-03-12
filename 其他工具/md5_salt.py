#
#暴力破解如下md5加密方式：md5(md5($pass).$salt)
#

from hashlib import md5
import threading
from optparse import OptionParser

def opTions():
    usage="%prog -c <ciphertext> -s <salt> -f <pwd_file> -t <thread>"
    parser = OptionParser(usage=usage)
    parser.add_option('-c',dest="ciphertext",help="指定密文")
    parser.add_option('-s',dest="salt",help="指定盐")
    parser.add_option('-f','--file',dest="filename",help="指定密码字典")
    parser.add_option('-t',dest="thread",help="指定线程数")
    options,args = parser.parse_args()
    return options

def get_args():
    args = opTions()
    ciphertext = args.ciphertext
    salt = args.salt
    filename = args.filename
    thread = args.thread
    return ciphertext,salt,filename,thread

class MyThread(threading.Thread):

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args[0],self.args[1],self.args[2])

def encode_md5_salt(pwd,salt,ciphertext):
    pool_sema.acquire()
    pwd1 = pwd
    pwd_md5 = md5(pwd.encode("utf-8")).hexdigest()
    pwd_md5_salt = md5((pwd_md5+salt).encode("utf-8")).hexdigest()
    if pwd_md5_salt == ciphertext:
        print("解密成功:")
        print(ciphertext+"对应的明文为:"+pwd1)
    pool_sema.release()


if __name__ == '__main__':
    ciphertext, salt, filename, thread = get_args()
    with open(filename, 'r') as f:
        pwds = f.readlines()
    print('密码总数：' + str(len(pwds)))
    thread_list = []
    max_connections = 50 
    if thread:
        max_connections = thread
    pool_sema = threading.BoundedSemaphore(max_connections)
    for pwd in pwds:
        m = MyThread(encode_md5_salt, (pwd.strip(),salt.strip(),ciphertext.strip(),))
        thread_list.append(m)

    for mt in thread_list:
        mt.start()

    for mt in thread_list:
        mt.join()
