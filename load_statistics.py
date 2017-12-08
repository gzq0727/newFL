#coding=utf-8
import os
import time

if __name__ == '__main__':
    with open('load_ratio.txt','w') as fr:
	p1_last_bytes = 0.0
	p2_last_bytes = 0.0
	index = 1
	while(True):
        	result = os.popen('ovs-ofctl -O openflow15 dump-flows s4')
        	res = result.read()
        	for line in res.splitlines():
	 	    if 'cookie=0x1' in line:
			splits = line.split(',')
			p1_bytes = float(splits[4].split('=')[-1])
			p1_bytes_transmit = p1_bytes - p1_last_bytes
			p1_last_bytes = p1_bytes

        	result = os.popen('ovs-ofctl -O openflow15 dump-flows s3')
        	res = result.read()
        	for line in res.splitlines():
			if 'cookie=0x2' in line:
			    splits = line.split(',')
			    p2_bytes = float(splits[4].split('=')[-1])
			    p2_bytes_transmit = p2_bytes - p2_last_bytes
			    p2_last_bytes = p2_bytes
        	
		load_ratio = p1_bytes_transmit / p2_bytes_transmit if p2_bytes_transmit != 0  else 'inf'
		if load_ratio != 'inf':
		    fr.write(str(index)+ '\t' +str(load_ratio)+'\n')
		    fr.flush()
		    index = index + 1
    		#flow record time interval
        	time.sleep(0.3)
