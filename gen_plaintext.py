#!/usr/bin/env python3

# This script will generate permutations of possible plaintext passphrases
# for specific passphrase length
# - Single thread since overhead for multithread seems so big i.e. slower
# - Write out in small chunks to save RAM space

import os
import itertools
import sys
from time import sleep

#generate plaintext 
#small subset since too much time to calculate hash
charlist = """ABCDE"""
charlen = 9
combitn = len(charlist)**charlen
#formula is length ^characters

pathfile = os.getcwd()
namefile = 'RUNNING ' + str(charlen) + '-char-plaintext.txt'
outfile = os.path.join(pathfile,namefile)

# entire printable ASCII 
# !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"abcdefghijklmnopqrstuvwxyz{|}~

sys.stdout.write('\n\033[33m SERIAL: Running... \n\n\033[0m')

li=[]

try:
	with open(outfile,'w') as f:
		#permutation 
		for k,i in enumerate(itertools.product(charlist,repeat=charlen)):
			li.append(''.join(i))
		
			if (k%200==0):
				f.write('\n'.join(li) )
				f.write('\n')	
				li=[]

#			add sleep for every million
			if (k !=0 and k%1000000==0):
				sleep(3)
				print("Sleep for 3 seconds:","[%d%%]" % (k/combitn *100), format(k,',d'),"of",format(combitn,',d') )
		
		f.write('\n'.join(li) )
		print("\n Generated",format(k+1, ',d'), "phrases")
		
	os.rename(namefile,namefile[8:])			
	print(" \n Done")

except KeyboardInterrupt:
	sys.stdout.write('\033[33m') #terminal colour
	sys.stdout.write('\n User Interrupt \n')
	sys.stdout.write('\033[0m')	#reset color	
	print("Killed at", format(k,',d') , li[-1] )


