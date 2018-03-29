#Outputs data to excel file with counts per gene
import sys
from operator import itemgetter

def countSorted(path): 
	file1 = open('C:/Zid/SolexaDataAnalysis/EYp35Timecourse/1Pp35Feat.txt','r')
	output = open('C:/Zid/SolexaDataAnalysis/EYp35Timecourse/1Pp35Sorted.txt','w')
	temp = file1.readline()
	line1 = temp.rstrip() 
	temp1 = line1.split('\t')
	Name = temp1[0]
	ChrT = Name[2]
	Chr = '1'
	dct_lst = [{"name":temp1[0],"Start":temp1[1],"End":"7236","Posit":temp1[3],"Count":temp1[4]}]

	for line in file1 :
   		temp = line.rstrip()
   		temp1 = temp.split('\t')
     
   		temp_lst = [{"name":temp1[0],"Start":temp1[1],"End":temp1[2],"Posit":temp1[3],"Count":temp1[4]}]
   		dct_lst.extend(temp_lst)
	file1.close()

	#for line in file2:
  
	#   temp = line.rstrip()
	#   temp1 = temp.split('\t')  
	#   temp_lst = [{"name":temp1[0],"Start":temp1[1],"End":temp1[2],"Posit":temp1[3],"Count":temp1[4],"ASCount": temp1[5]}]
	#   dct_lst.extend(temp_lst)

	#file2.close()


	dct_lst.sort(key=itemgetter("name"))


	for i in range(len(dct_lst)) :
   		output.write(dct_lst[i]["name"]+'\t'+dct_lst[i]["Start"]+'\t'+dct_lst[i]["End"]+'\t'+dct_lst[i]["Posit"]+'\t'+dct_lst[i]["Count"]+'\n') #sense count
      
	output.close()

	file1 = open(path)
	output = open('C:/Zid/SolexaDataAnalysis/EYp35Timecourse/1Pp35Counted.txt','w')
	output.write('Name\tStrt\tEnd\tLength\tCount\tStallCount\tCodeCount\t200Count\t200EndCount\n')


	tName = 'YAL001C'
	tStrt = 147596
	tEnd = 151168
	tLength = 3573
	tCount = 0
	Count =0
	SCount = 0
	CCount = 0
	CountS = 0
	CountE = 0

	for line in file1:
    		temp = line.rstrip()
    		temp1 = temp.split('\t')
    		Name = temp1[0]
   
    		if Name[0] == 'Q':
        		Count = 0
    		elif Name[0] == 'Y':
        		Strt = int(temp1[1])
        		End = int(temp1[2])
        		Orien = Name[6]
        		Length = abs(Strt-End)
        		Posit = int(temp1[3])
        		tCount = int(temp1[4])
        		if tName == Name:
            			Count = Count + tCount
            			if Orien == 'W':
                			if Strt+20 > Posit and Strt-16 < Posit:
                    				SCount = SCount + tCount
                			elif Strt+220 > Posit and Strt-16 < Posit:
                    				CountS = CountS + tCount
                			elif End - 200 < Posit:
                    				CountE = CountE + tCount

            			elif Orien == 'C':
                			if Strt-20 < Posit and Strt+16 > Posit:
                    				SCount = SCount + tCount
                			elif Strt-220 < Posit and Strt+16 > Posit:
                    				CountS = CountS + tCount
                			elif End + 200 > Posit:
                    				CountE = CountE + tCount

        			else :
            				CCount = Count - SCount
            				output.write(tName+'\t'+str(tStrt)+'\t'+str(tEnd)+'\t'+str(tLength)+'\t'+str(Count)+'\t'+str(SCount)+'\t'+str(CCount)+'\t'+str(CountS)+'\t'+str(CountE)+'\n')
            				Count =0
            				SCount = 0
            				CCount = 0
            				CountS = 0
            				CountE = 0
            				tName = Name
            				Count = Count + tCount
            				tStrt = Strt
            				tEnd = End
            				tLength = Length
            				if Orien == 'W':
                				if Strt+20 > Posit and Strt-16 < Posit:
                    					SCount = SCount + tCount
                				elif Strt+220 > Posit and Strt-16 < Posit:
                    					CountS = CountS + tCount
                				elif End - 200 < Posit:
                    					CountE = CountE + tCount

            				elif Orien == 'C':
                				if Strt-20 < Posit and Strt+16 > Posit:
                    					SCount = SCount + tCount
                				elif Strt-220 < Posit and Strt+16 > Posit:
                    					CountS = CountS + tCount
                				elif End + 200 > Posit:
                    					CountE = CountE + tCount
	outputpath = 'C:/Zid/SolexaDataAnalysis/EYp35Timecourse/1Pp35Counted.txt'
	output.close()
	return outputpath
