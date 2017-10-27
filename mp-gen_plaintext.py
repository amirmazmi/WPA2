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

pathfile = os.getcwd()
namefile = 'mp-plaintext'
outfile = os.path.join(pathfile,namefile)

#generate plaintext - small subset since too much time to calculate hash


# wpa_passphrase cannot handle quotes
#	!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

def gen_text(comb):
	ptext = (''.join(comb))
	q.put(ptext)
#	print(ptext, os.getpid())
	return 0

if __name__=='__main__':
	charlist = """ABC"""
	sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
	sys.stdout.flush()

	try:
		q=mp.Queue()		
		with open(outfile,'w') as f:

			#permutation 
#			perm = itertools.product(charlist,repeat=8)
			with mp.Pool(mp.cpu_count()) as pool:
				result = pool.imap( gen_text, (itertools.product(charlist,repeat=8)))
				k=0
				que=[]
				while (1):
					try:
						que.append(q.get(timeout=0.1))
						
						if (k%10==0 and k!=0):
							f.write('\n'.join(que)) 
							f.write('\n')
							que=[]
#						print(k,que)
						k+=1
					except queue.Empty:
						f.write('\n'.join(que)) 
						print("\n\n", k,"exit while loop")
						break
				q.close()
			print("\n Generated",format(k, ',d'), "phrases")
				
		print(" \n Done")

	except KeyboardInterrupt:
		q.close()
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
		print("Killed at", k, que[-1])
		sys.stdout.write('\033[0m')	#reset color

