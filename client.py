# -*- coding: utf-8 -*-
from socket import *
import time
import random
import multiprocessing
import threading
import numpy as np
from scipy.stats import poisson
from scipy.stats import norm

def sendAsRate(localAddress,localPort,remoteAddr,remotePort,rate = 10):
    client = socket(AF_INET, SOCK_STREAM)
    client.bind((localAddress, localPort))
    client.connect((remoteAddr, remotePort))
    BUFSIZE = 2048
    
    #发包的时间间隔服从poisson分布
    mu = 500 #poisson分布的强度，平均发送时间间隔
    loc = 1  #发送时间间隔的最小值
    send_times = 1*1000000/mu  #1s内的send次数
    try:
        while True:
            time_interval_series = poisson.rvs(mu, loc, send_times)# 生成send之间时间间隔序列
            
	    average_data_size = rate * (10**6) / 8 /send_times - 58  #按照发送速率和发包次数计算出的每个data的平均大小
            data_size_list = norm.rvs(average_data_size, 2, send_times)
            random.shuffle(data_size_list)
	    
	    last_time = time.time()
            for j in range(len(data_size_list)):
                data = ''
                for k in range(int(data_size_list[j]) if int(data_size_list[j]) > 0 else 1):  # 1KB = 966Bytes data + 58Bytes header
                    data += '1'
                client.send(data.encode('utf8'))
                data = client.recv(BUFSIZE)
                #print data
		time_shift =  time.time() - last_time
		#print time_shift
		last_time = time.time()
		sleep_time = float(time_interval_series[j])/(10**6) - time_shift 
                time.sleep(sleep_time if sleep_time > 0 else 0 )
    except BaseException as e:
        print e.message
    finally:
        client.close()
	
def sendMax(localAddress,localPort,remoteAddr,remotePort):
    client = socket(AF_INET, SOCK_STREAM)
    client.bind((localAddress, localPort))
    client.connect((remoteAddr, remotePort))
    BUFSIZE = 1024
    data_chunk = ''
    for i in range(1000):
	data_chunk += '1'	

    try:
        while True:
            data = data_chunk
            for i in range(2):#每次发送data的大小影响吞吐量
                data += data
            client.send(data.encode('utf-8'))
            #data = client.recv(BUFSIZE)
	    time.sleep(0.0001)
            #print data
    except BaseException as e:
        print e.message
    finally:
        client.close()

def getFCT(localAddress,localPort,remoteAddr,remotePort,fileSize=1):#unit MB
    client = socket(AF_INET, SOCK_STREAM)
    client.bind((localAddress, localPort))
    client.connect((remoteAddr, remotePort))
    BUFSIZE = 1024
    fileSize = fileSize * (10**6) / 1024

    data_count = 0
    startTime = time.time()
    try:
        while True:
            data = ''
            for i in range(966):#每次发送data的大小影响吞吐量
                data += '1'
            client.send(data.encode('utf8'))
            data = client.recv(BUFSIZE)
	    data_count += len(data)
	    print 'fize size:'+str(fileSize) + ' sent_count:' + str(data_count)
	    if data_count > fileSize:
		    break
        client.send('@'.encode('utf-8'))
        wait_start_time = time.time()
        while True:
    	    checkString = client.recv(BUFSIZE)
	    print checkString
            wait_end_time = time.time()
            if '@' in checkString.decode('utf-8') and wait_end_time - wait_start_time < 2 :
	        endTime = time.time()
	        print 'FCT:'+ str(endTime - startTime)
	        break
	    elif wait_end_time - wait_start_time >= 2:
	        print 'timeout'
	        break
  	client.close()
    except BaseException as e:
	print e.massage
    finally:
  	client.close()

if __name__ == '__main__':
    
    processings = []
    client_num = 6 
    rate = 8
    for i in range(client_num):
	#t = multiprocessing.Process(target=sendAsRate,args=('172.18.0.2',4000+i,'172.18.0.1',5000,rate))
	#t = multiprocessing.Process(target=sendAsRate,args=('192.168.1.186',4000+i,'192.168.1.185',5000,rate))
	#t = multiprocessing.Process(target=getFCT,args=('192.168.1.186',4000+i,'192.168.1.185',3001,10))
	#t = multiprocessing.Process(target=sendMax,args=('192.168.1.186',4000+i,'192.168.1.185',6000))
	t = multiprocessing.Process(target=sendMax,args=('172.18.0.2',4000+i,'172.18.0.1',6000))
        processings.append(t)

    for processing in processings:
        processing.daemon = True
        processing.start()
    processing.join()
    
    #sendMax('192.168.1.186',3000,'192.168.1.185',3001)
