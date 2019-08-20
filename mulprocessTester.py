#!/usr/bin/python3
#-*-coding:utf-8-*-

import zipfile
import optparse
import queue as Queue
import threading
import time

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

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
    def run(self):
        print('[*] Starting thread-' + self.name)
        while True:
            try:
                ectF(self.name, self.q)
            except:
                break
        print('[*] Exiting thread-' + self.name)

def ectF(name, q):
    passwd = q.get(timeout=1)
    try:
        zF.extractall(pwd=passwd)
        print('[+] Found Password: ' + bytes.decode(passwd) + '\n')
    except:
        pass

def main():
    threads = []
    workQueue = Queue.Queue(0)
    threadList = []
    for j in range(20):
        tName = str(j)
        thread = myThread(tName, workQueue)
        thread.start()
        threads.append(thread)
    for u in pF.readlines():
        passwd1 = str.encode(u.strip("\n"))
        workQueue.put(passwd1)
    for t in threads:
        t.join()
    end = time.time()
    print(end-start)

if __name__ == "__main__":
    main()
