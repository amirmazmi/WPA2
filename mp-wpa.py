#!/usr/bin/env python3

#https://www.binpress.com/tutorial/simple-python-parallelism/121

# This script generates the plaintext passphrase for a specific length
# and generates the hash using the cli tool wpa_passphrase.
# - Attempt to use multiple cores

# improvements
# 1. write permutations out straight to file
# 2. read permutation from file in chunks, hash and append


import subprocess as sub
import itertools
import sys
import multiprocessing as mp
import datetime as dt


def getHash(phrase):
	#generate hash
	proc = sub.run("wpa_passphrase mywifi " + phrase, shell="TRUE", stdout=sub.PIPE, universal_newlines="TRUE")
	output = proc.stdout.split()

	psk = (phrase, output[3][4:])
	return psk


# wpa_passphrase cannot handle quotes
#	!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

if __name__=='__main__':
	li=[]
	charlist = """a2Pd"""

	try:
		sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
		startTime = dt.datetime.now()

		#permutation 
		li = [''.join(i) for i in itertools.product(charlist, repeat = 8)]
		sampli = li[:15000]

		with mp.Pool(2) as pool:
			result = pool.map( getHash, sampli)
			endTime = dt.datetime.now()

		print("\n Plaintext permutations:", format(len(li), ',d') )
		print(" Hash calculated:", format(len(result), ',d'),"\n" )
		# length output is 64
		# 32 bytes; 8 word
		
		timeTaken = (endTime - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		hashpersec = len(sampli)/timeTaken.total_seconds()

#			[print("%s:%s" % (result[i][0], result[i][1], len(result[i][1])/2)) for i in range(len(result)) ]

		print("     Total time taken:", 
						" \n\t minutes:", format(minDuration,  '.3f'), 
						" \n\t seconds:", format( timeTaken.total_seconds(), '.3f' ))
		print("     Hash per second:", format( hashpersec, '.3f') )

		sys.stdout.write('\n\033[33m ### DONE ### \n\n\n\033[0m')
		
	except KeyboardInterrupt:
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
		sys.stdout.write('\033[0m')	#reset color


