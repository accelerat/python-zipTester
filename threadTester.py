#!/usr/bin/python3
#-*-coding:utf-8-*-

from multiprocessing import Pool, Manager
import time
import optparse
import zipfile

pwd = []
with open("wordlist.txt", "r") as file:
    for eachone in file.readlines():
        pwd.append(eachone.replace('\n', '').encode())

parser = optparse.OptionParser("usage%prog " + "-f <zipfile> -d <dictionary>")
parser.add_option("-f", dest="zname", type="string", help="specify zip file")
parser.add_option("-d", dest="dname", type="string", help="specify dictionary file")
(options, args) = parser.parse_args()
if (options.zname == None) | (options.dname == None):
    print(parser.usage)
    exit(0)
else:
    zname = options.zname
    dname = options.dname
zF = zipfile.ZipFile(zname)
pF = open(dname)

start = time.time()
def ectF(q, index):
    Process_id = 'Process-' + str(index)
    while not q.empty():
        passwd = q.get(timeout=1)
        try:
            zF.extractall(pwd=passwd)
            print("[+] Found Password: " + bytes.decode(passwd) + '\n')
        except Exception as err:
            pass

if __name__ == '__main__':
    manager = Manager()
    workQueue = manager.Queue(0)

    for passwd in pwd:
        workQueue.put(passwd)

    pool = Pool(processes=10)
    for i in range(11):
        pool.apply_async(ectF, args=(workQueue, i))

    pool.close()
    pool.join()
    end = time.time()

    print(end-start)
