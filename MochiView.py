import os
def MochiView(path)
	file1 = open(path,'r')
	output = open('/home/rchancha/Bowtie/bowtie/MochiView/5Pp35_comb_Mochi.txt', 'w')
	output.write('SEQ_NAME\tSTART\tEND\tSTRAND\tCOUNT\n')
	#temp7 = file1.readline()
	norm = 2.65 # Normalized to total alignable reads/3 million

	for line in file1:
	    temp = line.rstrip()
	    temp1 = temp.split('\t') 
    	    name = "Chr"+temp1[1]
       
            PositTemp = int(temp1[3])
            Orien = temp1[0]
    	if Orien == '+' :
        	count = (float(temp1[2]))/norm
        	Start = str(PositTemp)
        
    	else :
        	tempc = (float(temp1[2]))/norm
        	count = tempc*(-1)
        	Start = str(PositTemp)
        
    	output.write(name+'\t'+Start+'\t'+Start+'\t'+Orien+'\t'+str(count)+ '\n')  #antisense count
	outputpath = '/home/rchancha/Bowtie/bowtie/MochiView/5Pp35_comb_Mochi.txt'
	output.close()
	file1.close()
	return outputpath
