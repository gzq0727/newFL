#-*- coding: utf-8 -*-
from socket import *
import multiprocessing
import threading
from time import ctime
from time import localtime
import time

def recvAsRateHandler(TCPClientSock,TCPClientAddr):
    BUFSIZE = 8192
    data_count = 0;
    try:
        start_time = time.time()
        while True:
            data = TCPClientSock.recv(BUFSIZE)
            #print len(data)
            end_time = time.time()
            data_count += (len(data) + 58)
	    if(end_time - start_time > 5):
            	print str(TCPClientAddr) + ' '+str(data_count) + ' bytes '+ str(data_count * 8 / 1024 / (end_time - start_time)/1000 )+' Mb/s\n'  # Kb/s
                data_count = 0
  	    	start_time = end_time
	    #TCPClientSock.send('#'.encode('utf-8'))
            # time.sleep(0.1)
    except BaseException as e:
        print e.message
        TCPClientSock.close()

def getFCTHandler(TCPClientSock,TCPClientAddr):
    BUFSIZE = 2048
    while True:
        data = TCPClientSock.recv(BUFSIZE)
       	#print data
	if '@' in data.decode('utf-8'):
	    TCPClientSock.send('@'.encode('utf-8'))
	    print 'flow is completed'
	    break
	else:
	    TCPClientSock.send('1'.encode('utf-8'))
	
if __name__ == '__main__':
    #localAddress = '192.168.1.185'
    localAddress = '172.18.0.1'
    localPort = 6000
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((localAddress, localPort))
    server.listen(10)
  
    t = None
    while True:
        TCPClientSock, TCPClientAddr = server.accept()
        #t = multiprocessing.Process(target=getFCTHandler,args=(TCPClientSock, TCPClientAddr))
        t = multiprocessing.Process(target=recvAsRateHandler,args=(TCPClientSock, TCPClientAddr))
        t.daemon = True
        t.start()
    t.join()


