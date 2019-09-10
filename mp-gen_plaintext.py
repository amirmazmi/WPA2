#!/usr/bin/env python3

# This script will generate permutations of possible plaintext passphrases
# for specific passphrase length
# - attemps to use all cores - but has significant overhead
# - Write out in small chunks to save RAM space


import os
import itertools
import sys
import multiprocessing as mp
from time import sleep
import queue


charlen = 7
charlist = """ABCDEFGHIJK"""
combitn = len(charlist)**charlen       #formula is length ^characters

pathfile = os.getcwd()
namefile = 'RUNNING ' + str(charlen+1) + '-char-plaintext.txt'
outfile = os.path.join(pathfile,namefile)

#generate plaintext - small subset since too much time to calculate hash


# wpa_passphrase cannot handle quotes
#	!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

def gen_text(comb):
	ptext = (''.join( ("A",)+comb) )
	q.put(ptext)
#	print(ptext, os.getpid())
	return 0

if __name__=='__main__':
	
	sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
	sys.stdout.flush()

	try:
		print("\t Generating ", format(combitn,',d'), "combinations...\n")
		startTime = dt.datetime.now()
		q=mp.Queue()		
		with open(outfile,'w') as f:

			#permutation 
#			perm = itertools.product(charlist,repeat=8)
			with mp.Pool(mp.cpu_count()) as pool:
				result = pool.imap( gen_text, (itertools.product(charlist,repeat=charlen)))
				k=0
				que=[]
				while (1):
					try:
						que.append(q.get(timeout=0.1))
						
						if (k%500==0 and k!=0):
							print("\t Length should be 500:", length(que) )
							f.write('\n'.join(que)) 
							f.write('\n')
							que=[]
#						print(k,que)
						k+=1
						
					except queue.Empty:
						f.write('\n'.join(que)) 
						f.write('\n')
						print("\n\n\t Exiting while loop")
						break
				
				q.close()
		f.close()
		os.rename(namefile,namefile[8:])			
			
		print("\n\t Generated",format(k, ',d'), "phrases")
	
		timeTaken = (dt.datetime.now() - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		print("     Total time taken", 
				" \n\t minutes:", format(minDuration,  '.3f'), 
				" \n\t seconds:", format( timeTaken.total_seconds(), '.3f' ),
				"\n\t rate   :", format(  k/(timeTaken.total_seconds()*10**6), '.2f' ), "million phrases per second"	)


	sys.stdout.write('\n\n\033[33m ### DONE ### \n\n\n\033[0m')

	except KeyboardInterrupt:
		q.close()
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
		print("Killed at", k, que[-1])
		sys.stdout.write('\033[0m')	#reset color
		
		
		