#!/usr/bin/env python3

# This script will generate permutations of possible plaintext passphrases
# for specific passphrase length
# - Single thread since overhead for multithread seems so big i.e. slower
# - Write out in small chunks to save RAM space

import os
import itertools
import sys
import datetime as dt
from time import sleep

#generate plaintext 
#small subset since too much time to calculate hash
charlist = """ABCDEFGH"""
charlen = 7
combitn = len(charlist)**charlen       #formula is length ^characters

sleepdur = 1

pathfile = os.getcwd()
namefile = 'RUNNING ' + str(charlen+1) + '-char-plaintext.txt'
outfile = os.path.join(pathfile,namefile)

# entire printable ASCII 
# !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"abcdefghijklmnopqrstuvwxyz{|}~

sys.stdout.write('\n\033[33m SERIAL: Running... \n\033[0m')

li=[]

try:
	print("\t Generating ", format(combitn,',d'), "combinations...\n")
	startTime = dt.datetime.now()
	with open(outfile,'w') as f:
		#permutation 
		for k,i in enumerate(itertools.product(charlist,repeat=charlen)):
			li.append(''.join( ("A",)+i) )
		
			if (k%100000==0):
				f.write('\n'.join(li) )
				f.write('\n')	
				li=[]

#			add sleep for every 10 million
			if (k !=0 and k%10000000==0):
				sleep(sleepdur)
				print("Sleep for",sleepdur, "seconds:","[%d%%]" % (k/combitn *100), format(k,',d'),"of",format(combitn,',d') )
		
		f.write('\n'.join(li) )
		f.write('\n')
		print("\n Generated",format(k+1, ',d'), "phrases")
	
	f.close()
	os.rename(namefile,namefile[8:])			

	timeTaken = (dt.datetime.now() - startTime)
	minDuration = timeTaken/dt.timedelta(seconds=60)

	print("     Total time taken", 
					" \n\t minutes:", format(minDuration,  '.3f'), 
					" \n\t seconds:", format( timeTaken.total_seconds(), '.3f' ),
					"\n\t rate   :", format(  k/(timeTaken.total_seconds()*10**6), '.2f' ), "million phrases per second"	)


	sys.stdout.write('\n\n\033[33m ### DONE ### \n\n\n\033[0m')


except KeyboardInterrupt:
	sys.stdout.write('\033[33m') #terminal colour
	sys.stdout.write('\n User Interrupt \n')
	sys.stdout.write('\033[0m')	#reset color	
	print("Killed at", format(k,',d') , li[-1] )

