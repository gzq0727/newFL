if __name__ == '__main__':
    with open('congst_fl_log.txt','r') as f:
        with open('congst_fl_s2.txt', 'w') as f2:
            with open('congst_fl_s2_p1.txt', 'w') as f3:
                with open('congst_fl_s2_p2.txt', 'w') as f4:
	  	    index2 = 1
		    index3 = 1
		    index4 = 1
                    allline = f.readlines()
                    for line in allline:
                        splits = line.split(' ')
                        if splits[0] == 's2' and splits[60] != '0.000000':
                            f2.write(str(index2) + '\t' +splits[60] + '\t' + splits[62])
			    index2 = index2 + 1
                        if splits[0] == 's2' and splits[58] == '1' and splits[60] != '0.000000':
                            f3.write(str(index3)+ '\t' +splits[60] + '\t' + splits[62])
			    index3 = index3 + 1
                        elif splits[0] == 's2' and splits[58] == '2' and splits[60] != '0.000000':
                            f4.write(str(index4)+ '\t' +splits[60]+ '\t' + splits[62])
			    index4 = index4 + 1
